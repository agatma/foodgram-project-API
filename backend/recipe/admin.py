
from django.contrib import admin

from recipe.models import Ingredient, FavoriteRecipe, Recipe, IngredientAmountInRecipe, Tag, ShoppingCart


class TagAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "color",
        "slug",
    )


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "measurement_unit",
    )


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "text", "image", "author", "cooking_time")
    list_editable = ("name", "text", "image", "author", "cooking_time")


class IngredientAmountInRecipeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "recipe",
        "ingredient",
        "amount",
    )
    list_filter = ("id", "recipe", "ingredient")


class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "recipe",
    )


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "recipe",
    )
    list_filter = ("user",)


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(FavoriteRecipe, FavoriteRecipeAdmin)
admin.site.register(IngredientAmountInRecipe, IngredientAmountInRecipeAdmin)
