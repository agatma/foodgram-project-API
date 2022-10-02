from django.contrib import admin

from recipe.models import (
    FavoriteRecipe, Ingredient, IngredientAmountInRecipe, Recipe, ShoppingCart, Tag
)


class TagAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "color",
        "slug",
    )
    search_fields = (
        "name",
    )


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "measurement_unit",
    )
    search_fields = (
        "name",
    )


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "text", "image", "author", "cooking_time")
    list_editable = ("name", "text", "image", "author", "cooking_time")
    search_fields = (
        "name", "author"
    )


class IngredientAmountInRecipeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "recipe",
        "ingredient",
        "amount",
    )
    list_filter = ("recipe", "ingredient")
    search_fields = (
        "recipe",
    )


class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "recipe",
    )
    list_filter = ("user", "recipe")
    search_fields = (
        "recipe",
    )


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "recipe",
    )
    list_filter = ("user", "recipe")
    search_fields = (
        "recipe",
    )


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(FavoriteRecipe, FavoriteRecipeAdmin)
admin.site.register(IngredientAmountInRecipe, IngredientAmountInRecipeAdmin)
