from django.db import models
from django.utils import timezone

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

    class Meta:
        ordering = ['-popularity']
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    def __str__(self):
        """String representation of the Article object."""
        return self.title

    def get_labels_list(self):
        """Returns labels as a list of strings."""
        if self.labels:
            return [label.strip() for label in self.labels.split(',')]
        return []

    def save(self, *args, **kwargs):
        """
        Override save method to clean labels before saving.
        Ensures consistent format for labels storage.
        """
        if self.labels:
            # Clean and standardize labels format
            labels_list = self.get_labels_list()
            self.labels = ', '.join(labels_list)
        super().save(*args, **kwargs)