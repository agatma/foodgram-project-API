from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from api.views import (CustomUserViewSet, IngredientViewSet,
                       RecipePostDeleteFavoriteView, RecipeViewSet, ShoppingCartDownloadView,
                       ShoppingCartPostDeleteView, SubscribePostDeleteView,
                       SubscribeListViewSet, TagViewSet)

router = DefaultRouter()
router.register("tags", TagViewSet, basename="tags")
router.register("ingredients", IngredientViewSet, basename="ingredients")
router.register("recipes", RecipeViewSet, basename="recipes")

router.register("users/subscriptions", SubscribeListViewSet, basename="subscriptions")
router.register(r"users", CustomUserViewSet, basename="users")

urlpatterns = [
    path(r"recipes/download_shopping_cart/", ShoppingCartDownloadView.as_view()),
    path(r"users/<int:pk>/subscribe/", SubscribePostDeleteView.as_view()),
    path("", include(router.urls)),
    path("", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
    path(r"recipes/<int:pk>/favorite/", RecipePostDeleteFavoriteView.as_view()),
    path(r"recipes/<int:pk>/shopping_cart/", ShoppingCartPostDeleteView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

schema_view = get_schema_view(
    openapi.Info(
        title="Foodgram API",
        default_version="v1",
        description="ƒÓÍÛÏÂÌÚ‡ˆËˇ ‰Îˇ ÔËÎÓÊÂÌËˇ api ÔÓÂÍÚ‡ Foodgram",
        contact=openapi.Contact(email="admin@mail.ru"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    url(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    url(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    url(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]
