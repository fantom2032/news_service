import requests
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView


class ArticleProxyView(APIView):
    def get(self, request):
        url = f"https://newsapi.org/v2/everything?q=technology&language=ru&apiKey={settings.NEWS_API_KEY}"
        response = requests.get(url).json()
        return Response(response.get("articles", []))
