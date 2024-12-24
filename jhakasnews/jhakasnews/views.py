from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from .models import Article

def home(request):
    """
    View function for the home page of the news website.
    Implements pagination to display 10 articles per page.
    """
    # Get all articles ordered by publication date
    article_list = Article.objects.all().order_by('-popularity')
    
    # Create a paginator object with 10 articles per page
    paginator = Paginator(article_list, 10)
    
    # Get the page number from the request
    page = request.GET.get('page', 1)
    
    try:
        # Get the articles for the requested page
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        articles = paginator.page(paginator.num_pages)
    
    # Prepare the context dictionary
    context = {
        'articles': articles,
        'page': int(page),
        'total_pages': paginator.num_pages,
    }
    
    return render(request, 'home.html', context)

def article_detail(request, article_id):
    """
    View function for displaying individual article details.
    """
    try:
        article = Article.objects.get(id=article_id)
        context = {'article': article}
        return render(request, 'article_detail.html', context)
    except Article.DoesNotExist:
        return HttpResponse("Article not found", status=404)

def category_view(request, category):
    """
    View function for displaying articles by category.
    Implements pagination for category-specific articles.
    """
    article_list = Article.objects.filter(category=category).order_by('-publication_date')
    
    paginator = Paginator(article_list, 10)
    page = request.GET.get('page', 1)
    
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    
    context = {
        'articles': articles,
        'page': int(page),
        'total_pages': paginator.num_pages,
        'category': category
    }
    
    return render(request, 'category.html', context)