from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.postgres.fields import ArrayField
from django.conf import settings

class Article(models.Model):
    """
    Model representing a news article with basic fields for title, content, date, and labels.
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
    views = models.IntegerField(default=0)

    vector_embedding = ArrayField( models.FloatField(), size=1024, # adjust according to the embedding dimension 
                                  null=True, blank=True, )

    class Meta:
        ordering = ['-views']
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
    def str(self):
        """String representation of the Article object."""
        return self.title
    def get_labels_list(self):
        """Returns labels as a list of strings."""
        if self.labels:
            return [label.strip() for label in self.labels.split(',')]
        return []
    def save(self, args, **kwargs):
        """
        Override save method to clean labels before saving.
        Ensures consistent format for labels storage.
        """
        if self.labels:
            # Clean and standardize labels format
            labels_list = self.get_labels_list()
            self.labels = ', '.join(labels_list)
        super().save(args, **kwargs)

class ActiveArticles(models.Model):
    article = models.OneToOneField(
        'Article',
        on_delete=models.CASCADE,
        primary_key=True
    )

    class Meta:
        managed = False
        db_table = 'articles_article'
        default_permissions = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in Article._meta.fields:
            if field.name != 'id':
                setattr(self, field.name, getattr(self.article, field.name, None))

    @staticmethod
    def get_queryset():
        week_ago = timezone.now() - timedelta(days=7)
        return Article.objects.filter(date_added__gte=week_ago)

    def save(self, *args, **kwargs):
        if not hasattr(self, 'article'):
            self.article = Article()
        
        for field in Article._meta.fields:
            if field.name != 'id':
                setattr(self.article, field.name, getattr(self, field.name, None))
        
        self.article.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.article.delete()
        super().delete(*args, **kwargs)


from django.db import models
from django.contrib.auth.models import User

class UserInteractions(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='all_user_interactions')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='all_article_interactions')
    session_id = models.CharField(max_length=255)
    clicked = models.BooleanField(default=False)
    time_spent = models.IntegerField(default=0)  # Time spent in seconds

    def __str__(self):
        return f"{self.user.username} - {self.article.title} - {self.session_id}"
