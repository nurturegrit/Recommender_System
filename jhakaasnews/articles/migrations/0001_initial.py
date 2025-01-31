# Generated by Django 5.1.4 on 2024-12-25 06:11

import django.contrib.postgres.fields
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Enter the article headline', max_length=200)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now, help_text='Date and time when the article was added')),
                ('text', models.TextField(help_text='Enter the article content')),
                ('labels', models.CharField(blank=True, help_text='Enter comma-separated labels for the article', max_length=100)),
                ('views', models.IntegerField(default=0)),
                ('vector_embedding', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), blank=True, null=True, size=1024)),
            ],
            options={
                'verbose_name': 'Article',
                'verbose_name_plural': 'Articles',
                'ordering': ['-views'],
            },
        ),
        migrations.CreateModel(
            name='ActiveArticles',
            fields=[
                ('article', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='articles.article')),
            ],
            options={
                'db_table': 'articles_article',
                'managed': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='UserInteractions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(max_length=255)),
                ('clicked', models.BooleanField(default=False)),
                ('time_spent', models.IntegerField(default=0)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='all_article_interactions', to='articles.article')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='all_user_interactions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
