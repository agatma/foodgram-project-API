from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        _('Название'),
        max_length=200,
        unique=True
    )
    color = models.CharField(
        _('Цвет'),
        max_length=7,
        null=True,
        blank=False
    )
    slug = models.SlugField(
        _('Ссылка'),
        max_length=200,
        unique=True,
        null=True,
        blank=False
    )

    class Meta:
        ordering = ('name',)
        verbose_name = _('тег')
        verbose_name_plural = _('теги')

    def __str__(self):
        return f'Тег {self.name}'


class Ingredient(models.Model):
    name = models.CharField(
        _('Название'),
        max_length=200,
        null=False
    )
    measurement_unit = models.CharField(
        _('Единица измерения'),
        max_length=30,
        null=False
    )

    class Meta:
        ordering = ('name',)
        verbose_name = _('ингредиент')
        verbose_name_plural = _('ингредиенты')

    def __str__(self):
        return f'Ингредиент: {self.name} - {self.measurement_unit}'


class Recipe(models.Model):
    author = models.ForeignKey(
        to=User,
        verbose_name=_('Автор'),
        related_name='recipes',
        null=True,
        on_delete=models.SET_NULL
    )
    name = models.CharField(
        _('Название'),
        max_length=200,
        null=False,
        blank=False
    )
    text = models.CharField(
        _('Описание'),
        max_length=1024,
        blank=False,
        null=False,
    )
    ingredients = models.ManyToManyField(
        to=Ingredient,
        through='IngredientAmountInRecipe',
        related_name='recipes',
        verbose_name=_('Ингредиенты'),
    )
    tags = models.ManyToManyField(
        to=Tag,
        related_name='recipes',
        verbose_name=_('Теги'),
    )
    image = models.ImageField(
        _('Изображение'),
        upload_to='media/',
        null=True,
        default=None
    )
    cooking_time = models.PositiveIntegerField(
        _('Время приготовления'),
        validators=(MinValueValidator(1, 'Время приготовления должно быть больше минуты'),))

    date = models.DateTimeField(
        _('Дата публикации'),
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-date',)
        verbose_name = _('рецепт')
        verbose_name_plural = _('рецепты')

    def __str__(self):
        return f'{self.name} - Время приготовления {self.cooking_time}'


class IngredientAmountInRecipe(models.Model):
    recipe = models.ForeignKey(
        to=Recipe,
        related_name='ingredients_in_recipe',
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        to=Ingredient,
        related_name='ingredients_in_recipe',
        on_delete=models.CASCADE
    )
    amount = models.PositiveIntegerField(
        _('Количество'),
        validators=(MinValueValidator(1, 'Количество должно быть больше или равно одному'),))

    class Meta:
        verbose_name = _('Количество ингредиентов')
        verbose_name_plural = _('Количество ингредиентов')


