import requests
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from rest_framework.generics import ListAPIView
from django.utils.timezone import now, timedelta
from .models import Article
from .serializers import ArticleSerializer


class ArticleUpdateView(APIView):
    def post(self, request):
        return self._update()

    def get(self, request):  
        return self._update()

    def _update(self):
        cache_key = "articles_update"
        if cache.get(cache_key):
            return Response({"detail": "Используйте кэш"}, status=200)

        url = f"https://newsapi.org/v2/everything?q=technology&language=ru&apiKey={settings.NEWS_API_KEY}"
        response = requests.get(url).json()
        new_articles = []

        for item in response.get("articles", []):
            if not Article.objects.filter(url=item["url"]).exists():
                article = Article.objects.create(
                    source_id=item["source"].get("id") if item.get("source") else None,
                    source_name=item["source"].get("name") if item.get("source") else None,
                    author=item.get("author"),
                    title=item.get("title"),
                    description=item.get("description"),
                    url=item.get("url"),
                    url_to_image=item.get("urlToImage"),
                    published_at=item.get("publishedAt"),
                    content=item.get("content"),
                )
                new_articles.append(article.title)

        cache.set(cache_key, True, 60 * 30)
        return Response({"added": new_articles})

class ArticleListView(ListAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        fresh = self.request.query_params.get("fresh")
        title_contains = self.request.query_params.get("title_contains")

        if fresh == "true":
            qs = qs.filter(published_at__gte=now() - timedelta(hours=24))
        if title_contains:
            qs = qs.filter(title__icontains=title_contains)

        return qs

    def list(self, request, *args, **kwargs):
        cache_key = f"articles_{request.get_full_path()}"
        data = cache.get(cache_key)
        if data:
            return Response(data)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, 600)
        return response
