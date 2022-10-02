"""Модуль для установки дополнительных разрешений.
"""

from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """
    Разрешение на изменение только для автора.
    Остальным только чтение объекта.
    """

    def has_object_permission(self, request, view, obj):
        return (
                request.method in ('GET',)
                or (request.user == obj)
                or request.user.is_staff
        )


class AdminOrReadOnly(permissions.BasePermission):
    """
    Разрешение на создание и изменение только для администраторов.
    Остальным только чтение объекта.
    """

    def has_permission(self, request, view):
        return (
                request.method in ('GET',)
                or request.user.is_authenticated
                and request.user.is_staff
        )


class UserAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Разрешение на создание и изменение для авторизованных и для администраторов.
    Остальным только чтение объекта, кроме адреса api/users/me
    """

    def has_permission(self, request, view):
        return (
                (request.method in ('GET',) and 'me' not in request.path)
                or request.user.is_authenticated
                and request.user.is_staff
        )
