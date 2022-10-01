"""Модуль для создания, настройки и управления моделями пакета `recipe`.

Models:
    Recipe:
        Главная модель приложения, через которую описываются рецепты.
        Связана с моделями: Tag, Ingredient, IngredientAmountInRecipe,
        FavoriteRecipe, ShoppingCart
    Tag:
       Модель для группировки рецептов по тегам (завтрак, обед, ужин и тд.).
       Связана с Recipe через Many-To-Many.
    Ingredient:
        Модель для описания ингредиентов.
        Загрузка ингредиентов происходит через команду python manage.py loader
        Связана с Recipe через модель IngredientAmountInRecipe (Many-To-Many).
    IngredientAmountInRecipe:
        Модель для связи ингредиентов (Ingredient) и рецептов (Recipe)
        Также указывает количество ингредиента.
    FavoriteRecipe:
        Модель для добавления и исключения рецептов из избранных
        Связана внешним ключом с моделью Recipe и User
    ShoppingCart:
        Модель для добавления и исключения рецептов из списка покупок
        Связана внешним ключом с моделью Recipe и User
"""

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Tag(models.Model):
    """Теги для рецептов.
    Связано с моделью Recipe через М2М.
    Поля name и slug - обязательны для заполнения.
    Attribute:
        name(str):
            Название. Установлены ограничения по длине и уникальности.
        color(str):
            Цвет в HEX-кодировке. По умолчанию - IndianRed
        slug(str):
            Латинское наименование тега
    Examples:
        Tag('Завтрак', '#CD5C5C', 'breakfast')
        Tag('Обед', '#DD5CFF', 'launch')
        """
    name = models.CharField(
        _("name"),
        max_length=200,
        unique=True,
        default="Без категории"
    )
    color = models.CharField(
        _("color"),
        max_length=7,
        null=False,
        blank=False,
        default="#CD5C5C"
    )
    slug = models.SlugField(
        _("slug"),
        max_length=200,
        unique=True,
        null=False,
        blank=False,
        default="without_category"

    )

    class Meta:
        ordering = ("name",)
        verbose_name = "тег"
        verbose_name_plural = "теги"

    def __str__(self):
        return f"Тег {self.name}"


class Ingredient(models.Model):
    """Ингредиенты для рецепта.
    Attribute:
        name(str):
            Название ингредиента.
            Установлены ограничения по длине и уникальности.
        measurement_unit(str):
            Единицы измерения ингредиенты (граммы, штуки, литры и т.п.).
            Установлены ограничения по длине.
    Examples:
        Ingredient("Помидоры", "г"),
        Ingredient("Яйца", "штук")
    """
    name = models.CharField(
        _("name"),
        max_length=200,
        null=False
    )
    measurement_unit = models.CharField(
        _("Measurement unit"),
        max_length=30,
        null=False
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "ингредиент"
        verbose_name_plural = "ингредиенты"
        constraints = (
            models.UniqueConstraint(
                fields=("name", "measurement_unit"), name="unique_ingredient"
            ),
        )

    def __str__(self):
        return f"Ингредиент: {self.name} - {self.measurement_unit}"


class Recipe(models.Model):
    """Модель для рецептов.
    Attribute:
        name(str):
            Название рецепта. Установлены ограничения по длине.
            Дополнительное ограничение на стороне БД (null=False, blank=False)
        author(User):
            Автор рецепта. Связан с моделью User через ForeignKey.
        tags(Tags):
            Связь M2M с моделью Tag.
        ingredients(IngredientAmountInRecipe):
            Связь M2M с моделью Ingredient. Связь создаётся через модель
            IngredientAmountInRecipe с указанием количества ингредиентов.
        date(datetime):
            Дата добавления рецепта. Прописывается автоматически.
        image(str):
            Изображение рецепта. Указывает путь к изображению.
        text(str):
            Описание рецепта. Установлены ограничения по длине.
            Дополнительное ограничение на стороне БД (null=False, blank=False)
        cooking_time(int):
            Время приготовления рецепта.
            Установлено ограничение по минимальному значению (больше 1-ой минуты)
    """

    author = models.ForeignKey(
        to=User,
        verbose_name=_("Автор"),
        related_name="recipes",
        null=True,
        on_delete=models.SET_NULL,
    )
    name = models.CharField(
        _("Название"),
        max_length=200,
        null=False,
        blank=False
    )
    text = models.CharField(
        _("Описание"),
        max_length=1024,
        blank=False,
        null=False,
    )
    ingredients = models.ManyToManyField(
        to=Ingredient,
        through="IngredientAmountInRecipe",
        related_name="recipes",
        verbose_name=_("Ингредиенты"),
    )
    tags = models.ManyToManyField(
        to=Tag,
        related_name="recipes",
        verbose_name=_("Теги"),
    )
    image = models.ImageField(
        _("Изображение"),
        upload_to="media/",
        null=True,
        default=None
    )
    cooking_time = models.PositiveIntegerField(
        _("Время приготовления"),
        validators=(
            MinValueValidator(1, "Время приготовления должно быть больше минуты"),
        ),
    )

    date = models.DateTimeField(
        _("Дата публикации"),
        auto_now_add=True,
    )

    class Meta:
        ordering = ("-date",)
        verbose_name = _("рецепт")
        verbose_name_plural = _("рецепты")

    def __str__(self):
        return f"{self.name} - Время приготовления {self.cooking_time}"


class IngredientAmountInRecipe(models.Model):
    """Количество ингредиентов в рецепте.
    Модель связывает две модели: Recipe и Ingredient.
    Attribute:
        recipe(Recipe):
            Связь с моделью Recipe через ForeignKey.
        ingredients(int):
            Связь с моделью Ingredient через ForeignKey.
        amount(int):
            Количество ингредиентов. Установлено ограничение
            по минимальному значению.
    Examples:
        IngredientAmountInRecipe(Recipe instance, Ingredient instance, 10)
        IngredientAmountInRecipe(Recipe instance, Ingredient instance, 25)
    """
    recipe = models.ForeignKey(
        to=Recipe,
        related_name="ingredients_in_recipe",
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        to=Ingredient,
        related_name="ingredients_in_recipe",
        on_delete=models.RESTRICT
    )
    amount = models.PositiveIntegerField(
        _("Количество"),
        validators=(
            MinValueValidator(1, "Количество должно быть больше или равно одному"),
        ),
    )

    class Meta:
        verbose_name = _("Количество ингредиентов")
        verbose_name_plural = _("Количество ингредиентов")


class FavoriteRecipe(models.Model):
    """Подписка на любимые рецепты.
    Модель связывает две модели: Recipe и User.
    Установлено ограничение на уникальность этой комбинации.
    Attribute:
        recipe(Recipe):
            Связь с моделью Recipe через ForeignKey.
        user(User):
            Связь с моделью User через ForeignKey.
        added_date(datetime):
            Время подписки. Добавляется автоматически
    Examples:
        FavoriteRecipe(Recipe instance, User instance)
        FavoriteRecipe(Recipe instance, User instance)
    """
    recipe = models.ForeignKey(
        to=Recipe,
        related_name="favorite_recipe",
        on_delete=models.CASCADE,
        verbose_name=_("Рецепт"),
    )
    user = models.ForeignKey(
        to=User,
        related_name="favorite_recipe",
        on_delete=models.CASCADE,
        verbose_name=_("Автор"),
    )
    added_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Дата добавления")
    )

    class Meta:
        verbose_name = _("Избранное")
        verbose_name_plural = _("Избранное")
        constraints = (
            models.UniqueConstraint(
                fields=("recipe", "user"), name="unique_favorite_recipe"
            ),
        )


class ShoppingCart(models.Model):
    """Добавление товара в список покупок.
    Модель связывает две модели: Recipe и User.
    Установлено ограничение на уникальность этой комбинации.
    Attribute:
        recipe(Recipe):
            Связь с моделью Recipe через ForeignKey.
        user(User):
            Связь с моделью User через ForeignKey.
    Examples:
        ShoppingCart(Recipe instance, User instance)
        ShoppingCart(Recipe instance, User instance)
    """
    user = models.ForeignKey(
        to=User,
        related_name="shopping_cart",
        on_delete=models.CASCADE,
        verbose_name=_("Пользователь"),
    )
    recipe = models.ForeignKey(
        to=Recipe,
        related_name="shopping_cart",
        on_delete=models.CASCADE,
        verbose_name=_("Корзина"),
    )

    class Meta:
        verbose_name = _("Корзина")
        verbose_name_plural = _("Корзина")
        constraints = (
            models.UniqueConstraint(
                fields=("recipe", "user"), name="unique_recipe_in_shopping_cart"
            ),
        )
