from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import mixins, pagination, status, viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response

from api.filters import RecipeFilter, IngredientFilter
from api.serializers import (
    IngredientSerializer,
    RecipeFavoriteSerializer,
    RecipeSerializer,
    SubscribeSerializer,
    TagSerializer,
    CustomUserSerializer,
)
from recipe.models import FavoriteRecipe, Ingredient, Recipe, Tag
from users.models import Subscribe

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
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class RecipeFavoriteView(GenericAPIView):
    print("Вызвана")
    queryset = Recipe.objects.all()
    serializer_class = RecipeFavoriteSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        _, created = FavoriteRecipe.objects.get_or_create(
            recipe=self.get_object(), user=request.user
        )
        if created:
            return Response(
                data=self.get_serializer(self.get_object()).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        obj = FavoriteRecipe.objects.filter(recipe=self.get_object(), user=request.user)
        if obj.exists():
            obj.first().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class SubscribeListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = pagination.LimitOffsetPagination


class SubscribeCreateDestroyView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        author = self.get_object()
        _, created = Subscribe.objects.get_or_create(user=request.user, author=author)
        if author == request.user or not created:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        instance = Subscribe.objects.filter(user=request.user, author=self.get_object())
        if instance.exists():
            instance.first().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = TagSerializer
    pagination_class = None
