import base64
from django.core.files.base import ContentFile
from rest_framework import serializers
from recipe.models import Tag, Ingredient, Recipe, IngredientAmountInRecipe
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


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
            "amount"
        )


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            ext = format.split("/")[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f"temp.{ext}")
        return super().to_internal_value(data)


class RecipeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=200,
        allow_null=False,
        allow_blank=False,
        required=True
    )
    text = serializers.CharField(
        max_length=1024,
        allow_null=False,
        allow_blank=False,
        required=True
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        required=True,
    )
    ingredients = IngredientAmountSerializer(
        source="ingredients_in_recipe",
        many=True,
        required=True
    )
    image = Base64ImageField(
        allow_null=True,
        required=True
    )
    author = CustomUserSerializer(read_only=True)
    cooking_time = serializers.IntegerField(
        min_value=1,
        required=True
    )

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
        )

    def create(self, validated_data):
        ingredients = validated_data.pop("ingredients_in_recipe")
        tags = validated_data.pop("tags")
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        recipe.ingredients_in_recipe.set(
            IngredientAmountInRecipe.objects.create(
                recipe=recipe, ingredient=i.get("id"), amount=i.get("amount")
            )
            for i in ingredients
        )
        return recipe


class RecipeFavoriteSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )