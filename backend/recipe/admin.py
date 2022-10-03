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
        "name", "color", "slug"
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
    list_filter = ("measurement_unit",)


class IngredientInRecipeAdmin(admin.TabularInline):
    model = IngredientAmountInRecipe
    fk_name = 'recipe'


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "author", "amount_favorites", "amount_shopping")
    list_filter = ("tags",)

    search_fields = (
        "name", "author__username", "author__email"
    )
    inlines = (
        IngredientInRecipeAdmin,
    )

    @staticmethod
    @admin.display(description="В избранном, раз")
    def amount_favorites(obj):
        return obj.favorite_recipe.count()

    @staticmethod
    @admin.display(description="В списке покупок, раз")
    def amount_shopping(obj):
        return obj.shopping_cart.count()


class IngredientAmountInRecipeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "recipe",
        "ingredient",
        "amount",

    )
    search_fields = (
        "recipe__name", "recipe__author__username", "recipe__author__email"
    )


class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "recipe",
    )
    search_fields = (
        "recipe__name", "user__username", "user__email"
    )
    list_filter = ("recipe__tags",)


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "recipe",
    )
    search_fields = (
        "recipe__name", "user__username", "user__email"
    )
    list_filter = ("recipe__tags",)


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(FavoriteRecipe, FavoriteRecipeAdmin)
admin.site.register(IngredientAmountInRecipe, IngredientAmountInRecipeAdmin)
