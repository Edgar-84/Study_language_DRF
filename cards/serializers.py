from rest_framework import serializers

from .models import Card, Category


class CardListSerializer(serializers.ModelSerializer):
    """View list cards"""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Card
        fields = ("id", "user", "category", "title_native_language", "translate_studied_language")

    def create(self, validated_data):
        category_data = validated_data.get('category')
        user_info = validated_data.get('user')

        if category_data in Category.objects.filter(user=user_info):
            result = Card.objects.create(**validated_data)
            return result
        else:
            raise serializers.ValidationError({"category": "you have entered a non-existent list"})


class CardDetailSerializer(serializers.ModelSerializer):
    """View all info about chosen card"""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Card
        fields = '__all__'


class CategoryListSerializer(serializers.ModelSerializer):
    """View list categories"""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Category
        fields = ("id", "user", "title")

    def create(self, validated_data):
        categories = Category.objects.filter(user=validated_data.get("user")).values_list('title', flat=True)
        if validated_data.get("title") in categories:
            raise serializers.ValidationError({"category": "Create failed. You have list with this name"})
        else:
            result = Category.objects.create(**validated_data)
            return result

    def update(self, instance, validated_data):
        categories = Category.objects.filter(user=validated_data.get("user")).values_list('title', flat=True)
        if validated_data.get("title") in categories:
            raise serializers.ValidationError({"category": "Update failed. You have list with this name"})
        else:
            instance = super(CategoryListSerializer, self).update(instance, validated_data)
            return instance


class CategoryDetailSerializer(serializers.ModelSerializer):
    """View all info about chosen category"""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Category
        fields = "__all__"
