from django.shortcuts import render, get_object_or_404
from django.db.models import F
from django.db import transaction
from django.contrib.auth.decorators import login_required
import numpy as np
import json
from scipy.spatial.distance import cosine
from .models import *
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import IntegrityError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

def index(request):
    query = request.GET.get('q')
    articles_all = ActiveArticles.objects.all() # Use ActiveArticles

    if query:
        articles_all = articles_all.filter(Q(title__icontains=query) | Q(text__icontains=query))

    featured_articles = ActiveArticles.objects.filter(featured=True) # Use ActiveArticles

    if featured_articles:
        articles_all = articles_all.exclude(pk__in=[article.pk for article in featured_articles])
        articles_all = list(featured_articles) + list(articles_all)

    paginator = Paginator(articles_all, 10)

    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    return render(request, 'articles/index.html', context={'articles': articles, 'query': query})

@require_POST
def update_interaction(request, article_id):
    data = json.loads(request.body)
    time_spent = data.get('time_spent')
    final_update = data.get('final_update', False)

    try:
        interaction, _ = UserInteractions.objects.get_or_create(
            user=request.user,
            article_id=article_id,
            session_id=request.session.session_key
        )
    except (KeyError, IntegrityError):
        return JsonResponse({'status': 'error', 'message': 'Invalid request data or interaction already exists'}, status=400)

    interaction.time_spent = time_spent
    interaction.clicked = final_update
    interaction.save()

    return JsonResponse({'status': 'success'})

def home(request):
    total_articles = 10

    featured_articles = ActiveArticles.objects.filter(featured=True)[:total_articles] # Use ActiveArticles
    featured_count = len(featured_articles)

    remaining_articles = total_articles - featured_count

    most_popular_articles = ActiveArticles.objects.order_by('-views')[:3] # Use ActiveArticles

    is_new_user = not request.user.is_authenticated or not hasattr(request.user, 'userprofile')

    remaining_articles_list = []
    if is_new_user:
        remaining_articles_list = most_popular_articles[:remaining_articles]
    else:
        remaining_articles_list = get_personalized_recommendations(request.user, remaining_articles)

    all_articles = list(featured_articles) + remaining_articles_list

    context = {
        'articles': all_articles,
        'featured_count': featured_count,
        'most_popular_articles': most_popular_articles,
        'is_new_user': is_new_user,
    }

    return render(request, 'articles/home.html', context)

def article_detail(request, article_id):
    article = get_object_or_404(ActiveArticles, id=article_id) # Use ActiveArticles

    with transaction.atomic():
        Article.objects.filter(id=article_id).update(views=F('views') + 1)
        article.refresh_from_db()

    recommended_articles = get_recommended_articles(article)

    context = {
        'article': article,
        'recommended_articles': recommended_articles,
    }

    return render(request, 'articles/article.html', context)

def get_personalized_recommendations(user, num_recommendations=3):
    try:
        user_profile = user.userprofile
    except UserProfile.DoesNotExist:
        return []

    normalized_profiles = user_profile.get_normalized_profiles()
    if not normalized_profiles['normalized_embedding']: #or not normalized_profiles['normalized_tfidf']:
        return []
    potential_recommendations = ActiveArticles.objects.exclude(userinteractions__user=user).exclude(vector_embedding__isnull=True)
    similarities = []
    for potential_article in potential_recommendations:
        similarity = 1 - cosine(
            np.array(normalized_profiles['normalized_embedding']),
            np.array(potential_article.vector_embedding)
        )
        similarities.append((potential_article, similarity))

    similarities.sort(key=lambda x: x[1], reverse=True)
    recommended_articles = [article for article, _ in similarities[:num_recommendations]]
    return recommended_articles

def get_recommended_articles(article, num_recommendations=3):
    potential_recommendations = ActiveArticles.objects.exclude(id=article.id)

    vector_recommendations = []
    if article.vector_embedding is not None:
        articles_with_vectors = potential_recommendations.exclude(vector_embedding__isnull=True)
        similarities = []
        for potential_article in articles_with_vectors:
            similarity = 1 - cosine(
                np.array(article.vector_embedding),
                np.array(potential_article.vector_embedding)
            )
            similarities.append((potential_article, similarity))

        similarities.sort(key=lambda x: x[1], reverse=True)
        vector_recommendations = [article for article, _ in similarities[:num_recommendations]]

    article_labels = set(article.get_labels_list())
    label_recommendations = []

    if article_labels:
        for potential_article in potential_recommendations:
            potential_labels = set(potential_article.get_labels_list())
            common_labels = article_labels.intersection(potential_labels)
            if common_labels:
                label_recommendations.append(
                    (potential_article, len(common_labels))
                )

        label_recommendations.sort(key=lambda x: x[1], reverse=True)
        label_recommendations = [article for article, _ in label_recommendations[:num_recommendations]]

    all_recommendations = []
    seen_ids = set()

    for article in vector_recommendations:
        if article.id not in seen_ids:
            all_recommendations.append(article)
            seen_ids.add(article.id)

    for article in label_recommendations:
        if article.id not in seen_ids and len(all_recommendations) < num_recommendations:
            all_recommendations.append(article)
            seen_ids.add(article.id)
    if len(all_recommendations) < num_recommendations:
        recent_articles = potential_recommendations.order_by('-date_added')
        for article in recent_articles:
            if article.id not in seen_ids and len(all_recommendations) < num_recommendations:
                all_recommendations.append(article)
                seen_ids.add(article.id)

    return all_recommendations