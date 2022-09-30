from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipe.models import FavoriteRecipe, Ingredient, Recipe, ShoppingCart, Tag
from rest_framework import mixins, pagination, viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from users.models import Subscribe

from api.filters import IngredientFilter, RecipeFilter
from api.mixins import RecipeActionPostDeleteGenericApiMixin, UserActionPostDeleteGenericApiMixin
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (CustomUserSerializer, IngredientSerializer,
                             RecipeSerializer, ShortRecipeSerializer,
                             SubscribeSerializer, TagSerializer)
from api.services import create_ingredients_file

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = pagination.LimitOffsetPagination


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = pagination.LimitOffsetPagination
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class RecipeFavoriteView(RecipeActionPostDeleteGenericApiMixin):
    queryset = Recipe.objects.all()
    serializer_class = ShortRecipeSerializer
    permission_classes = (IsAuthenticated,)
    action_model = FavoriteRecipe


class SubscribeListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = pagination.LimitOffsetPagination


class SubscribeCreateDestroyView(UserActionPostDeleteGenericApiMixin):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    action_model = Subscribe


class ShoppingCartView(RecipeActionPostDeleteGenericApiMixin):
    queryset = Recipe.objects.all()
    serializer_class = ShortRecipeSerializer
    permission_classes = (IsAuthenticated,)
    action_model = ShoppingCart


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = TagSerializer
    pagination_class = None


class ShoppingCartDownload(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return create_ingredients_file(request.user)

# Management
# https://github.com/AigulParamonova/foodgram-project-react/blob/master/backend/api/mixins.py
