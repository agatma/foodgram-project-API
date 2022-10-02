"""Модуль вспомогательных функций.
"""

from typing import List

from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse

from api.conf import FILENAME, CONTENT_TYPE, TOTAL_INGREDIENTS_HEADER
from recipe.models import IngredientAmountInRecipe

User = get_user_model()


def make_ingredients(user: User) -> str:
    """Записывает ингредиенты вложенные в рецепт.
    Создаёт объект IngredientAmountInRecipe связывающий объекты Recipe и
    Ingredient с указанием количества конкретного ингредиента.
    Returns:
        Список с суммарным количеством каждого ингредиента
    """
    ingredients = (
        IngredientAmountInRecipe.objects.filter(recipe__shopping_cart__user=user)
            .values("ingredient__name", "ingredient__measurement_unit")
            .annotate(Sum("amount"))
    )
    total_ingredients = TOTAL_INGREDIENTS_HEADER
    for ingredient in ingredients:
        name = ingredient["ingredient__name"]
        unit = ingredient["ingredient__measurement_unit"]
        amount = ingredient["amount__sum"]
        total_ingredients += f"{name} ({unit}) - {amount}\n"
    return total_ingredients


def create_ingredients_file(user: User) -> HttpResponse:
    """Добавляет в список ингредиентов заголовок и возвращает HttpResponse.
    """
    filename = FILENAME
    response = HttpResponse(
        make_ingredients(user=user),
        content_type=CONTENT_TYPE,
    )
    response["Content-Disposition"] = f"attachment; filename={filename}"
    return response
