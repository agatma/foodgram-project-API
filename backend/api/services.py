"""Модуль вспомогательных функций.
"""

from typing import List

from django.db.models import Sum
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from recipe.models import IngredientAmountInRecipe

User = get_user_model()


def make_ingredients_list(user: User) -> List[str]:
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
    total_ingredients = 'Список ингредиентов: \n\n'
    for ingredient in ingredients:
        name = ingredient["ingredient__name"]
        unit = ingredient["ingredient__measurement_unit"]
        amount = ingredient["amount__sum"]
        total_ingredients += f"{name} ({unit}) - {amount}\n"
    return total_ingredients


def create_ingredients_file(user: User) -> HttpResponse:
    """Добавляет в список ингредиентов заголовок и возвращает HttpResponse.
    """
    filename = "ingredients_to_buy.txt"
    response = HttpResponse(
        make_ingredients_list(user=user),
        content_type="text/plain; charset=UTF-8",
    )
    response["Content-Disposition"] = "attachment; filename={0}".format(filename)
    return response
