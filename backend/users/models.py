from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """Кастомный менеджер пользователей.
    Настроена идентификация по email вместо логина пользователя.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Создать и сохранить пользователя с указанными параметрами.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Создать и сохранить суперпользователя с указанными параметрами.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Настроенная под приложение Foodgram модель пользователя.
    При создании пользователя все поля обязательны для заполнения.
    Attribute:
        username(str):
            Логин пользователя.
            Установлены ограничения по максимальной длине.
            Дополнительное ограничение на стороне БД (null=False, blank=False)
        email(str):
            Адрес email пользователя
            Установлено ограничение по максимальной длине.
        first_name(str):
            Имя пользователя.
            Установлено ограничение по максимальной длине.
        last_name(str):
            Фамилия пользователя.
            Установлено ограничение по максимальной длине.
        password(str):
            Пароль для авторизации.
    """

    username = models.CharField(
        _("username"),
        blank=False,
        null=False,
        max_length=150,
        unique=True
    )
    email = models.EmailField(
        _("email address"),
        max_length=254,
        blank=False,
        null=False,
        unique=True
    )
    first_name = models.CharField(
        _("first name"),
        max_length=150
    )
    last_name = models.CharField(
        _("last name"),
        max_length=150
    )
    password = models.CharField(
        _("password"),
        max_length=150
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username", "first_name", "last_name")

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.email


class Subscribe(models.Model):
    """Подписка на пользователя.
    Модель связывает одну модель с собой: User c User.
    Установлено ограничение на уникальность этой комбинации.
    Attribute:
        user(User):
            Связь с моделью User через ForeignKey.
        author(User):
            Связь с моделью User через ForeignKey.
    Examples:
        Subscribe(User instance, User instance)
        Subscribe(User instance, User instance)
    """
    user = models.ForeignKey(
        to=CustomUser,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name="Подписчик",
    )
    author = models.ForeignKey(
        to=CustomUser,
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name="Автор",
    )

    class Meta:
        verbose_name = "Подписчик"
        verbose_name_plural = "Подписчики"
        constraints = (
            models.UniqueConstraint(
                fields=("user", "author"), name="unique_user_author"
            ),
        )
