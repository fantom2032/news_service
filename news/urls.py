from django.urls import path
from .views import ArticleProxyView

urlpatterns = [
    path("", ArticleProxyView.as_view(), name="articles"),
]