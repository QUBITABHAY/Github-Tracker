# githubdata/urls.py
from django.urls import path
from .views import github_user_data

urlpatterns = [
    path('github/<str:username>/', github_user_data, name='github_user_data'),
]
