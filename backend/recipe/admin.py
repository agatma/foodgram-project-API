from django.contrib import admin
from recipe.models import Tag, Ingredient, Recipe


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


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
