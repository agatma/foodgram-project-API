import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipe.models import (
    Ingredient,
    IngredientAmountInRecipe,
    Recipe,
    ShoppingCart,
    Tag,
)
from users.models import Subscribe

User = get_user_model()


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            ext = format.split("/")[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f"temp.{ext}")
        return super().to_internal_value(data)


class CustomUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
        )

    def get_is_subscribed(self, obj):
        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        return Subscribe.objects.filter(user=user, author=obj).exists()


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"


class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(
        source="ingredient.measurement_unit",
    )
    amount = serializers.IntegerField(min_value=1)

    class Meta:
        model = IngredientAmountInRecipe
        fields = (
            "id",
            "name",
            "measurement_unit",
            "amount",
        )

    def to_representation(self, instance):
        data = super(IngredientAmountSerializer, self).to_representation(instance)
        data["id"] = instance.ingredient.id
        return data


class RecipeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=200, allow_null=False, allow_blank=False, required=True
    )
    text = serializers.CharField(
        max_length=1024, allow_null=False, allow_blank=False, required=True
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        required=True,
    )
    ingredients = IngredientAmountSerializer(
        source="ingredients_in_recipe", many=True, required=True
    )
    image = Base64ImageField(allow_null=True, required=True)
    author = CustomUserSerializer(read_only=True)
    cooking_time = serializers.IntegerField(min_value=1, required=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "text",
            "tags",
            "ingredients",
            "image",
            "author",
            "cooking_time",
            "is_favorited",
            "is_in_shopping_cart",

        )

    @staticmethod
    def create_ingredients(ingredients, recipe):
        return (
            IngredientAmountInRecipe(
                recipe=recipe, ingredient=i.get("id"), amount=i.get("amount")
            )
            for i in ingredients
        )

    @staticmethod
    def validate_tags(data):
        if not data or len(set(data)) < len(data):
            raise serializers.ValidationError(
                {"tags": "Укажите подходящий уникальный тег (теги)"}
            )
        return data

    @staticmethod
    def validate_ingredients(data):
        if len({i["id"] for i in data}) < len(data):
            raise serializers.ValidationError(
                {"ingredients": "Ингредиенты должны быть уникальными"}
            )
        return data

    def get_is_favorited(self, obj):
        if self.context.get("request").user.is_anonymous:
            return False
        return (
            self.context.get("request").user.favorite_recipe.filter(recipe=obj).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        if self.context.get('request').user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            user=self.context.get('request').user, recipe=obj).exists()

    def create(self, validated_data):
        ingredients = validated_data.pop("ingredients_in_recipe")
        tags = validated_data.pop("tags")
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        IngredientAmountInRecipe.objects.bulk_create(
            self.create_ingredients(ingredients, recipe)
        )
        return recipe

    def update(self, recipe, validated_data):
        if "ingredients_in_recipe" in self.validated_data:
            ingredients = validated_data.pop("ingredients_in_recipe")
            recipe.ingredients.clear()
            IngredientAmountInRecipe.objects.bulk_create(
                self.create_ingredients(ingredients, recipe)
            )
        if "tags" in self.validated_data:
            tags = validated_data.pop("tags")
            recipe.tags.set(tags)
        return super().update(recipe, validated_data)


class ShortRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "cooking_time",
        )


class SubscribeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="author.pk")
    email = serializers.ReadOnlyField(source="author.email")
    username = serializers.ReadOnlyField(source="author.username")
    first_name = serializers.ReadOnlyField(source="author.first_name")
    last_name = serializers.ReadOnlyField(source="author.last_name")
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "recipes",
            "recipes_count",
            "is_subscribed",
        )
        validators = UniqueTogetherValidator(
            queryset=User.objects.all(), fields=("username", "id")
        )

    def get_recipes(self, obj):
        limit = self.context.get("request").query_params.get("recipes_limit")
        recipes = Recipe.objects.filter(author=obj.author)
        if limit:
            recipes = recipes[: int(limit)]
        serializer = ShortRecipeSerializer(recipes, many=True)
        return serializer.data

    @staticmethod
    def get_recipes_count(obj):
        return Recipe.objects.filter(author=obj.author).count()

    @staticmethod
    def get_is_subscribed(obj):
        return Subscribe.objects.filter(user=obj.user, author=obj.author).exists()


class ShoppingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = "__all__"
        validators = UniqueTogetherValidator(
            queryset=ShoppingCart.objects.all(), fields=("user", "recipe")
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"
