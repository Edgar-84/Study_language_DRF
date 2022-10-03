from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Card, Category
from .serializers import CardSerializer, CategorySerializer


class CardAPIList(generics.ListCreateAPIView):
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
