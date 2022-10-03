"""Модуль для установки дополнительных разрешений.
"""

from rest_framework import permissions


class IsAdminAuthorOrReadOnly(permissions.BasePermission):
    """Разрешено автору или администратору, остальные только для чтения"""

    def has_object_permission(self, request, view, obj):
        return (
                request.method in permissions.SAFE_METHODS
                or request.user.is_staff
                or obj.author == request.user
        )

    def has_permission(self, request, view):
        return (
                request.method in permissions.SAFE_METHODS or request.user.is_authenticated
        )


class AdminOrReadOnly(permissions.BasePermission):
    """
    Разрешение на создание и изменение только для администраторов.
    Остальным только чтение объекта.
    """

    def has_permission(self, request, view):
        return (
                request.method in ('GET',)
                or (request.user.is_authenticated and request.user.is_staff)
        )
