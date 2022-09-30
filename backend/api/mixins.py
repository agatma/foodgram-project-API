from django.contrib.auth import get_user_model
from django.db.models import Model
from recipe.models import Recipe
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

User = get_user_model()


class RecipeActionPostDeleteGenericApiMixin(GenericAPIView):
    action_model: Model = Recipe

    def post(self, request, *args, **kwargs):
        _, created = self.action_model.objects.get_or_create(
            recipe=self.get_object(), user=request.user
        )
        if created:
            return Response(
                data=self.get_serializer(self.get_object()).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        obj = self.action_model.objects.filter(
            recipe=self.get_object(), user=request.user
        )
        if obj.exists():
            obj.first().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserActionPostDeleteGenericApiMixin(GenericAPIView):
    action_model: Model = User

    def post(self, request, *args, **kwargs):
        _, created = self.action_model.objects.get_or_create(
            user=request.user, author=self.get_object()
        )
        if self.get_object() == request.user or not created:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        instance = self.action_model.objects.filter(
            user=request.user, author=self.get_object()
        )
        if instance.exists():
            instance.first().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
