import copy
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from cards.models import Card, Category
from cards.serializers import CardSerializer


class CardsTests(APITestCase):
    def setUp(self):
        user_test1 = User.objects.create_user(username='test1', password='1q2w3e4r5t')
        user_test1.save()

        user_test2 = User.objects.create_user(username='test2', password='123qwe')
        user_test2.save()

        self.user_test1_token = Token.objects.create(user=user_test1)
        self.user_test2_token = Token.objects.create(user=user_test2)

        self.client = APIClient()

        self.one_category = Category.objects.create(title="One_category", user=user_test1)
        self.one_card = Card.objects.create(
            user=user_test1,
            category=self.one_category,
            title_native_language='Test word',
            translate_studied_language='Translate_test_word',
        )

        self.data = {
            "title_native_language": "Мир",
            "translate_studied_language": "World",
            "category": self.one_category.id,
        }

    def test_cards_info_invalid(self):
        response = self.client.get(reverse("user_cards"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cards_info_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test1_token.key)
        response = self.client.get(reverse("user_cards"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cards_create_invalid(self):
        response = self.client.post(reverse("user_cards"), self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cards_create_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test1_token.key)
        response = self.client.post(reverse("user_cards"), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cards_detail_info_invalid(self):
        response = self.client.get(reverse("update_cards", kwargs={"pk": self.one_card.id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cards_detail_info_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test1_token.key)
        response = self.client.get(reverse("update_cards", kwargs={"pk": self.one_card.id}))
        serializer_data = CardSerializer(self.one_card).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, response.data)

    def test_cards_update(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test1_token.key)
        test_data = {"title_native_language": "Test word change",
                     "translate_studied_language": "Translate_test_word",
                     "category": self.one_category.id}

        response = self.client.put(reverse("update_cards", kwargs={"pk": self.one_card.id}), test_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title_native_language"], "Test word change")
        self.assertEqual(response.data["translate_studied_language"], "Translate_test_word")

    def test_category_create_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test1_token.key)
        response = self.client.post(reverse("user_category"), {"title": "Simple words"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Simple words")
