# users/urls.py
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('complete_profile/', views.CompleteProfileView.as_view(), name='complete_profile'),
]