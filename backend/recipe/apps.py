from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RecipeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recipe'
    verbose_name = _('Рецепт')
