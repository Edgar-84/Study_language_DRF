from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated

from .models import Card, Category
from .serializers import CardSerializer, CategorySerializer, SelectedCategorySerializer


class CardAPIList(generics.ListCreateAPIView):
    """View all cards current user"""
    serializer_class = CardSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Card.objects.filter(user=self.request.user)


class CardAPIUpdate(generics.RetrieveUpdateAPIView):
    serializer_class = CardSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return Card.objects.filter(user=self.request.user)


class CardAPIDestroy(generics.RetrieveDestroyAPIView):
    serializer_class = CardSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return Card.objects.filter(user=self.request.user)


class CategoryAPIList(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class CategoryAPIUpdate(generics.RetrieveUpdateAPIView):
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class CategoryAPIDestroy(generics.RetrieveDestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class SelectedCategoryCardsAPIList(generics.ListCreateAPIView):
    serializer_class = SelectedCategorySerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        if self.kwargs.get("pk") in Category.objects.filter(user=self.request.user).values_list(flat=True):
            return Card.objects.filter(user=self.request.user, category=self.kwargs["pk"])
        else:
            raise serializers.ValidationError({"category": "you have entered a non-existent list"})


