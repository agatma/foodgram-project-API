from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import mixins, viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from api.filters import IngredientFilter, RecipeFilter
from api.mixins import (RecipeActionPostDeleteMixin,
                        UserActionPostDeleteGenericApiMixin)
from api.permissions import AdminOrReadOnly, IsAdminAuthorOrReadOnly
from api.pagination import CustomPagination
from api.serializers import (CustomUserSerializer, IngredientSerializer,
                             RecipeSerializer, ShortRecipeSerializer,
                             SubscribeSerializer, TagSerializer)
from api.services import create_ingredients_file
from recipe.models import FavoriteRecipe, Ingredient, Recipe, ShoppingCart, Tag
from users.models import Subscribe

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """ViewSet для работы с пользователями."""
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = CustomPagination


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для работы с ингредиентами."""
    queryset = Ingredient.objects.all()
    permission_classes = AdminOrReadOnly,
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = DjangoFilterBackend,
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с рецептами."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = CustomPagination
    permission_classes = IsAdminAuthorOrReadOnly,
    filter_backends = DjangoFilterBackend,
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class RecipePostDeleteFavoriteView(RecipeActionPostDeleteMixin):
    """GenericApiView для добавления рецепта в избранное.
    Attribute:
        action_model_with_recipe: ModelWithAdditionalActionToRecipe
    """
    queryset = Recipe.objects.all()
    serializer_class = ShortRecipeSerializer
    permission_classes = IsAuthenticatedOrReadOnly,
    action_model_with_recipe = FavoriteRecipe


class SubscribeListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """ViewSet для работы с отображения списка подписок пользователя."""
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer
    permission_classes = IsAuthenticated,
    pagination_class = CustomPagination


class SubscribePostDeleteView(UserActionPostDeleteGenericApiMixin):
    """GenericApiView для добавления рецепта в список покупок.
    Attribute:
        action_model_with_user: ModelWithAdditionalActionToUser
    """
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = SubscribeSerializer
    action_model_with_user = Subscribe


class ShoppingCartPostDeleteView(RecipeActionPostDeleteMixin):
    """GenericApiView для добавления рецепта в список покупок.
    Attribute:
        action_model_with_recipe: ModelWithAdditionalActionToRecipe
    """
    queryset = Recipe.objects.all()
    serializer_class = ShortRecipeSerializer
    permission_classes = IsAuthenticated,
    action_model_with_recipe = ShoppingCart


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для работы с тегами."""
    queryset = Tag.objects.all()
    permission_classes = AdminOrReadOnly,
    serializer_class = TagSerializer
    pagination_class = None


class ShoppingCartDownloadView(GenericAPIView):
    """Представление для загрузки списка покупок"""
    permission_classes = IsAuthenticated,

    def get(self, request, *args, **kwargs):
        return create_ingredients_file(request.user)
