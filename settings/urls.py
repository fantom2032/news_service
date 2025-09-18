from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="News API",
        default_version="v1",
        description="Документация"
    ),
    public=True,
    permission_classes=[AllowAny],
)

def home(request):
    from news.models import Article  
    articles = Article.objects.all()
    return render(request, "core/index.html", {"articles": articles})

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    

    path("auth/", include("users.urls")),
    
    path("auth/jwt/create/", TokenObtainPairView.as_view(), name="jwt_create"),
    path("auth/jwt/refresh/", TokenRefreshView.as_view(), name="jwt_refresh"),
    
    path("articles/", include("news.urls")),
    
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-ui"),
]