from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Card, Category
from .serializers import (
    CardListSerializer,
    CardDetailSerializer,
    CategoryListSerializer,
    CategoryDetailSerializer,
)


class CardViewSet(viewsets.ModelViewSet):
    """View list cards"""

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Card.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ('list', 'create', 'update', 'destroy'):
            return CardListSerializer
        elif self.action == 'retrieve':
            return CardDetailSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """View list categories"""

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ('list', 'create', 'update', 'destroy'):
            return CategoryListSerializer
        elif self.action == 'retrieve':
            return CategoryDetailSerializer


class SelectedCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """View cards in selected category"""

    serializer_class = CardListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.kwargs.get("pk") in Category.objects.filter(user=self.request.user).values_list(flat=True):
            cards = Card.objects.filter(user=self.request.user, category=self.kwargs["pk"])
            return cards
        else:
            raise serializers.ValidationError({"category": "you have entered a non-existent list"})
