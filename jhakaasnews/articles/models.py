from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.postgres.fields import ArrayField
from django.conf import settings
from django.db.models import F
from django.contrib.auth.models import User
from .vectorizations import make_tfidf, make_embedding

class Article(models.Model):
    """
    Model representing a news article with basic fields for title, content, date, labels,
    and vector representations that are automatically generated upon saving.
    """
    title = models.CharField(
        max_length=200,
        help_text="Enter the article headline"
    )
    
    date_added = models.DateTimeField(
        default=timezone.now,
        help_text="Date and time when the article was added"
    )
    
    text = models.TextField(
        help_text="Enter the article content"
    )
    
    labels = models.CharField(
        max_length=100,
        help_text="Enter comma-separated labels for the article",
        blank=True
    )

    featured = models.BooleanField(default=False, null=False, blank=False)
    
    views = models.IntegerField(default=0)
    time_spent_on = models.IntegerField(default=0)
    
    vector_embedding = ArrayField(
        models.FloatField(),
        size=1024,  # adjust according to the embedding dimension
        null=True,
        blank=True,
    )
    
    tfidf_vector = ArrayField(
        models.FloatField(),
        size=1024,  # adjust according to your TF-IDF vector size
        null=True,
        blank=True,
    )
    
    class Meta:
        ordering = ['-views']
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    def __str__(self):
        return self.title

    def get_labels_list(self):
        if self.labels:
            return [label.strip() for label in self.labels.split(',')]
        return []

    def generate_vectors(self):
        """Generate TF-IDF and embedding vectors for the article content."""
        self.tfidf_vector = make_tfidf(self.text)
        self.vector_embedding = make_embedding(self.text)

    def save(self, *args, **kwargs):
        if self.labels:
            labels_list = self.get_labels_list()
            self.labels = ', '.join(labels_list)
        
        # Generate vectors for new articles or when text is updated
        if self._state.adding or self.tracker.has_changed('text'):
            self.generate_vectors()
        
        super().save(*args, **kwargs)

    def update_interaction_metrics(self, time_spent):
        """Update article metrics based on user interaction."""
        self.views = F('views') + 1
        self.time_spent_on = F('time_spent_on') + time_spent
        self.save()

class ActiveArticles(Article):
    """
    Proxy model for Article that only shows articles from the last 3 days.
    All operations on ActiveArticles objects directly affect the underlying Article objects.
    """
    class Meta:
        proxy = True
        
    @classmethod
    def get_queryset(cls):
        three_days_ago = timezone.now() - timedelta(days=3)
        return super().get_queryset().filter(date_added__gte=three_days_ago)
    
    def save(self, *args, **kwargs):
        # Ensure the date_added is within the last 3 days
        if not self.pk:  # New object
            self.date_added = timezone.now()
        super().save(*args, **kwargs)

class UserProfile(models.Model):
    """
    Extended user profile to store both embedding and TF-IDF vector representations
    of user interests along with interaction metrics.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vector_embedding_profile = ArrayField(
        models.FloatField(),
        size=1024,  # adjust according to embedding dimension
        null=True,
        blank=True,
    )
    tfidf_profile = ArrayField(
        models.FloatField(),
        size=1024,  # adjust according to TF-IDF dimension
        null=True,
        blank=True,
    )
    watched_articles = models.IntegerField(default=0)

    def initialize_vectors(self, vector_size):
        """Initialize vector profiles if they don't exist."""
        if not self.vector_embedding_profile:
            self.vector_embedding_profile = [0.0] * vector_size
        if not self.tfidf_profile:
            self.tfidf_profile = [0.0] * vector_size

    def update_profile_vectors(self, article, time_spent):
        """
        Update both embedding and TF-IDF profiles based on article interaction.
        Vectors are weighted by time spent and normalized by total articles watched.
        """
        if article.vector_embedding and article.tfidf_vector:
            vector_size = len(article.vector_embedding)
            self.initialize_vectors(vector_size)
            
            # Calculate weight based on time spent and watched articles
            weight = time_spent / (self.watched_articles + 1)
            
            # Update embedding profile
            self.vector_embedding_profile = [
                existing + (article_val * weight)
                for existing, article_val in zip(self.vector_embedding_profile, article.vector_embedding)
            ]
            
            # Update TF-IDF profile
            self.tfidf_profile = [
                existing + (article_val * weight)
                for existing, article_val in zip(self.tfidf_profile, article.tfidf_vector)
            ]
            
            self.watched_articles += 1
            self.save()

    def get_normalized_profiles(self):
        """
        Return normalized versions of both profile vectors.
        Useful for similarity calculations and recommendations.
        """
        def normalize_vector(vector):
            if not vector:
                return None
            magnitude = sum(x * x for x in vector) ** 0.5
            if magnitude == 0:
                return vector
            return [x / magnitude for x in vector]
        
        return {
            'normalized_embedding': normalize_vector(self.vector_embedding_profile),
            'normalized_tfidf': normalize_vector(self.tfidf_profile)
        }

class UserInteractions(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='all_user_interactions')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='all_article_interactions')
    session_id = models.CharField(max_length=255)
    clicked = models.BooleanField(default=False)
    time_spent = models.IntegerField(default=0)  # Time spent in seconds

    def __str__(self):
        return f"{self.user.username} - {self.article.title} - {self.session_id}"

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        
        if is_new and self.clicked:
            # Update article metrics
            self.article.update_interaction_metrics(self.time_spent)
            
            # Update user profile
            user_profile, created = UserProfile.objects.get_or_create(user=self.user)
            user_profile.update_profile_vectors(self.article, self.time_spent)
        
        super().save(*args, **kwargs)