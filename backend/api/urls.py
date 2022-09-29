from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from django.conf.urls import url

from api.views import (
    IngredientViewSet,
    RecipeViewSet,
    TagViewSet,
    SubscribeListViewSet,
    SubscribeCreateDestroyView,
    CustomUserViewSet,
    RecipeFavoriteView,
    ShoppingCartView,
)

router = DefaultRouter()
router.register("tags", TagViewSet, basename="tags")
router.register("ingredients", IngredientViewSet, basename="ingredients")
router.register("recipes", RecipeViewSet, basename="recipes")

router.register("users/subscriptions", SubscribeListViewSet, basename="subscriptions")
router.register(r"users", CustomUserViewSet, basename="users")

urlpatterns = [
    path("", include(router.urls)),
    path("", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
    path(r"recipes/<int:pk>/favorite/", RecipeFavoriteView.as_view()),
    path(r"recipes/<int:pk>/shopping_cart/", ShoppingCartView.as_view()),
    path(r"users/<int:pk>/subscribe/", SubscribeCreateDestroyView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

schema_view = get_schema_view(
    openapi.Info(
        title="Foodgram API",
        default_version="v1",
        description="Документация для приложения api проекта Foodgram",
        # terms_of_service="URL страницы с пользовательским соглашением",
        contact=openapi.Contact(email="admin@mail.ru"),
        license=openapi.License(name="BSD License"),
    ),
    public=True, permission_classes=(permissions.AllowAny,),
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
