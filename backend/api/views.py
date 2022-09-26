from rest_framework import viewsets, pagination, status
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from recipe.models import Tag, Ingredient, Recipe, FavoriteRecipe
from api.serializers import TagSerializer, IngredientSerializer, RecipeSerializer, RecipeFavoriteSerializer
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = AllowAny,
    serializer_class = IngredientSerializer
    pagination_class = None

    def get_queryset(self):  # sourcery skip: use-named-expression
        queryset = Ingredient.objects.all()
        name = self.request.query_params.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    pagination_class = pagination.LimitOffsetPagination
    permission_classes = IsAuthenticatedOrReadOnly,

    def get_queryset(self):
        queryset = Recipe.objects.prefetch_related("favorite_recipe")
        is_favorited = int(self.request.query_params.get("is_favorited", False))
        if is_favorited and self.request.user != 'AnonymousUser':
            queryset = queryset.filter(favorite_recipe__user=self.request.user)

        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=("POST", "DELETE"), permission_classes=(IsAuthenticated,))
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == "POST":
            if FavoriteRecipe.objects.get_or_create(recipe=recipe, user=request.user)[1]:
                return Response(data=RecipeFavoriteSerializer(recipe).data, status=status.HTTP_201_CREATED)
            return Response({"Ошибка": "Рецепт уже добавлен в избранное"}, status=status.HTTP_400_BAD_REQUEST)
        get_object_or_404(FavoriteRecipe, recipe=recipe, user=request.user).delete()
        return Response(data=RecipeFavoriteSerializer(recipe).data, status=status.HTTP_204_NO_CONTENT)
