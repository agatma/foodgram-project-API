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
    ShortRecipeSerializer,
    RecipeSerializer,
    SubscribeSerializer,
    TagSerializer,
    CustomUserSerializer,
    ShoppingSerializer,
)
from api.permissions import IsAuthorOrReadOnly
from recipe.models import FavoriteRecipe, Ingredient, Recipe, ShoppingCart, Tag
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
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class RecipeFavoriteView(GenericAPIView):
    queryset = Recipe.objects.all()
    serializer_class = ShortRecipeSerializer
    permission_classes = IsAuthenticated,

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


class ShoppingCartView(GenericAPIView):
    queryset = Recipe.objects.all()
    serializer_class = ShortRecipeSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        _, created = ShoppingCart.objects.get_or_create(
            recipe=self.get_object(), user=request.user
        )
        if created:
            return Response(
                data=self.get_serializer(self.get_object()).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        obj = ShoppingCart.objects.filter(recipe=self.get_object(), user=request.user)
        if obj.exists():
            obj.first().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = TagSerializer
    pagination_class = None

# @action(
#        methods=('GET',),
#        url_path='download_shopping_cart',
#        detail=False,
#        permission_classes=(IsAuthenticated,),
#     )
#     def download_shopping_cart(self, request):
#         user_id = request.user.id
#         list_of_ingredients = create_list_of_ingredients(user_id=user_id)
#
#         filename = 'list_of_ingredients.txt'
#         response = HttpResponse(
#             list_of_ingredients,
#             content_type='text/plain; charset=UTF-8',
#         )
#         response['Content-Disposition'] = (
#             'attachment; filename={0}'.format(filename)
#         )
#         return response




# from django.db.models import Sum
#
# from recipes.models import IngredientAmount
#
#
# def create_list_of_ingredients(user_id):
#     ingredients = IngredientAmount.objects.filter(
#         recipes__recipe_added_to_cart__user=user_id).values(
#             'name__name',
#             'name__measurement_unit'
#         ).annotate(Sum('amount'))
#     list_of_ingredients = 'Список ингредиентов: \n\n'
#     for ingredient in ingredients:
#         name = ingredient['name__name']
#         unit = ingredient['name__measurement_unit']
#         amount = ingredient['amount__sum']
#         list_of_ingredients += f'{name} ({unit}) - {amount}\n'
#     return list_of_ingredients