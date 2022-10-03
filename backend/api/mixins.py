"""Модуль содержит дополнительные классы
для настройки основных представлений приложения.
"""

from django.contrib.auth import get_user_model
from django.db.models import Model
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from recipe.models import Recipe

User = get_user_model()


class RecipeActionPostDeleteMixin(GenericAPIView):
    """Добавляет в GenericApiView методы Post и Delete.
    Mixin упрощает добавление дополнительных методов
    к основной модели Recipe: добавление в избранное,
    в корзину и т.д.
    Attribute:
        action_model_with_recipe(Recipe): AddToFavoriteModel
    """
    action_model_with_recipe: Model = Recipe

    def post(self, request, *args, **kwargs):
        _, created = self.action_model_with_recipe.objects.get_or_create(
            recipe=self.get_object(), user=request.user
        )
        if created:
            return Response(
                data=self.get_serializer(self.get_object()).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        obj = self.action_model_with_recipe.objects.filter(
            recipe=self.get_object(), user=request.user
        )
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserActionPostDeleteGenericApiMixin(GenericAPIView):
    """Добавляет в GenericApiView методы Post и Delete.
    Mixin упрощает добавление дополнительных методов
    к основной модели User: подписка, отписка, лайк и т.д.
    Attribute:
        action_model_with_user(Recipe): SubscribeToUserModel
    """
    action_model_with_user: Model = User

    def post(self, request, *args, **kwargs):
        if self.get_object() == request.user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        obj, created = self.action_model_with_user.objects.get_or_create(
            user=request.user, author=self.get_object()
        )
        if not created:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(
            data=self.get_serializer(obj).data,
            status=status.HTTP_201_CREATED,
        )

    def delete(self, request, *args, **kwargs):
        instance = self.action_model_with_user.objects.filter(
            user=request.user, author=self.get_object()
        )
        if instance.exists():
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
