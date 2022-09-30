from django_filters import rest_framework as filters
from recipe.models import Ingredient, Recipe


class RecipeFilter(filters.FilterSet):
    is_favorited = filters.BooleanFilter(
        field_name="is_favorited",
        method="favorite_filter"
    )
    is_in_shopping_cart = filters.BooleanFilter(
        field_name="is_in_shopping_cart",
        method="shopping_cart_filter"
    )
    tags = filters.AllValuesMultipleFilter(field_name="tags__slug")

    def favorite_filter(self, queryset, _, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(favorite_recipe__user=self.request.user)
        return queryset

    def shopping_cart_filter(self):
        return Recipe.objects.filter(shopping_cart__user=self.request.user)

    class Meta:
        model = Recipe
        fields = ("tags", "author")


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(
        field_name="name",
        method="filter_name"
    )

    @staticmethod
    def filter_name(queryset, _, value):
        return queryset.filter(name__icontains=value)

    class Meta:
        model = Ingredient
        fields = ("name",)
