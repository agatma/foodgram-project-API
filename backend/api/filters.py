from django_filters import rest_framework
from recipe.models import Recipe


class RecipeFilter(rest_framework.FilterSet):
    is_favorited = rest_framework.BooleanFilter(
        field_name='is_favorited',
        method='favorite_filter'
    )
    # is_in_shopping_cart = rest_framework.BooleanFilter(
    #     field_name='is_in_shopping_cart',
    #     method='shopping_cart_filter'
    # )
    tags = rest_framework.AllValuesMultipleFilter(field_name='tags__slug')

    def favorite_filter(self):
        return Recipe.objects.filter(favorite_recipe__user=self.request.user)

    # def shopping_cart_filter(self):
    #     return Recipe.objects.filter(shopping_cart__user=self.request.user)

    class Meta:
        model = Recipe
        fields = ['author']
