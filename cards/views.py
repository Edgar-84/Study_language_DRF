from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .models import Card
from .permissions import IsAdminOrReadOnly
from .serializers import CardSerializer


class CardAPIList(generics.ListCreateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )


class CardAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = (IsAuthenticated, )


class CardAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = (IsAdminOrReadOnly, )

