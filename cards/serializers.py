from rest_framework import serializers

from .models import Card, Category


class CardSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Card
        fields = '__all__'

    def create(self, validated_data):
        category_data = validated_data.get('category')
        user_info = validated_data.get('user')

        if category_data in Category.objects.filter(user=user_info):
            result = Card.objects.create(**validated_data)
            return result
        else:
            raise serializers.ValidationError({"category": "you have entered a non-existent list"})


class CategorySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Category
        fields = '__all__'

    def create(self, validated_data):
        categories = Category.objects.filter(user=validated_data.get("user")).values_list('title', flat=True)
        if validated_data.get("title") in categories:
            raise serializers.ValidationError({"category": "You have list with this name"})
        else:
            result = Category.objects.create(**validated_data)
            return result
