from django.urls import path
from .views import ArticleUpdateView, ArticleListView

urlpatterns = [
    path("update/", ArticleUpdateView.as_view(), name="article-update"),
    path("", ArticleListView.as_view(), name="article-list"),
]