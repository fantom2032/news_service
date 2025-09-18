from django.shortcuts import render
from news.models import News

def home(request):
    news_list = News.objects.all().order_by('-created_at')
    return render(request, "core/index.html", {"news_list": news_list})