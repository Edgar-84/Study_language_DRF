import copy
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from cards.models import Card, Category
from cards.serializers import CardSerializer, CategorySerializer


class CardsTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

        user_test1 = User.objects.create_user(username='test1', password='1q2w3e4r5t')
        user_test1.save()
        user_test2 = User.objects.create_user(username='test2', password='123qwe')
        user_test2.save()

        self.user_test1_token = Token.objects.create(user=user_test1)
        self.user_test2_token = Token.objects.create(user=user_test2)

        self.one_category = Category.objects.create(title="Category first user", user=user_test1)
        self.two_category = Category.objects.create(title="Category second user", user=user_test2)

        self.one_card = Card.objects.create(
            user=user_test1,
            category=self.one_category,
            title_native_language='Test word',
            translate_studied_language='Translate_test_word')

        self.two_card = Card.objects.create(
            user=user_test2,
            category=self.two_category,
            title_native_language="Word for delete",
            translate_studied_language="Translate word for delete")

        self.data = {
            "title_native_language": "Мир",
            "translate_studied_language": "World",
            "category": self.one_category.id}

    def test_cards_info_invalid(self):
        response = self.client.get(reverse("user_cards"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cards_info_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test1_token.key)
        response = self.client.get(reverse("user_cards"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Card.objects.all().count(), 2)
        self.assertEqual(response.data['count'], 1)

    def test_cards_create_invalid(self):
        response = self.client.post(reverse("user_cards"), self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cards_create_another_group_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test1_token.key)
        response = self.client.post(reverse("user_cards"), {"title_native_language": "Я",
                                                            "translate_studied_language": "I",
                                                            "category": self.two_category.id})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cards_create_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test1_token.key)
        response = self.client.post(reverse("user_cards"), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cards_detail_info_invalid(self):
        response = self.client.get(reverse("update_cards", kwargs={"pk": self.one_card.id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cards_detail_info_invalid_pk(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test1_token.key)
        response = self.client.get(reverse("update_cards", kwargs={"pk": self.two_card.id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cards_detail_info_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test1_token.key)
        response = self.client.get(reverse("update_cards", kwargs={"pk": self.one_card.id}))
        serializer_data = CardSerializer(self.one_card).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, response.data)

    def test_cards_update_invalid(self):
        response = self.client.put(reverse("update_cards", kwargs={"pk": self.one_card.id}), self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cards_update_invalid_pk(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test1_token.key)
        response = self.client.put(reverse("update_cards", kwargs={"pk": self.two_card.id}), self.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cards_update_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test1_token.key)
        response = self.client.put(reverse("update_cards", kwargs={"pk": self.one_card.id}), self.data)
        serializer_data = CardSerializer(Card.objects.get(pk=self.one_card.id)).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, response.data)

    def test_cards_delete_invalid(self):
        response = self.client.delete(reverse("delete_card", kwargs={"pk": self.one_card.id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cards_delete_invalid_id(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test1_token.key)
        response = self.client.delete(reverse("delete_card", kwargs={"pk": self.two_card.id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cards_delete_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test1_token.key)
        result = Card.objects.all()
        response = self.client.delete(reverse("delete_card", kwargs={"pk": self.one_card.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotEqual(result, Card.objects.all())

    def test_category_info_invalid(self):
        response = self.client.get(reverse("user_category"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_category_info_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test2_token.key)
        response = self.client.get(reverse("user_category"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(Category.objects.all().count(), 2)

    def test_category_create_invalid(self):
        response = self.client.post(reverse("user_category"), {"title": "Simple words"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_category_create_invalid_similar(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test1_token.key)
        response = self.client.post(reverse("user_category"), {"title": "Category first user"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_category_create_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test1_token.key)
        response = self.client.post(reverse("user_category"), {"title": "Simple words"})
        serializer_data = CategorySerializer(Category.objects.get(title="Simple words")).data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(serializer_data, response.data)

    def test_category_detail_info_invalid(self):
        response = self.client.get(reverse("update_category", kwargs={"pk": self.one_category.id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_category_detail_info_invalid_pk(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test1_token.key)
        response = self.client.get(reverse("update_category", kwargs={"pk": self.two_category.id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_category_detail_info_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test1_token.key)
        response = self.client.get(reverse("update_category", kwargs={"pk": self.one_category.id}))
        serializer_data = CategorySerializer(self.one_category).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, response.data)

    def test_category_update_invalid(self):
        response = self.client.put(reverse("update_category", kwargs={"pk": self.one_category.id}), {"title": "New"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_category_update_invalid_pk(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test1_token.key)
        response = self.client.put(reverse("update_category", kwargs={"pk": self.two_category.id}), {"title": "New"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_category_update_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test1_token.key)
        response = self.client.put(reverse("update_category", kwargs={"pk": self.one_category.id}), {"title": "New"})
        serializer_data = CategorySerializer(Category.objects.get(title="New")).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)

    def test_category_delete_invalid(self):
        response = self.client.delete(reverse("delete_category", kwargs={"pk": self.one_category.id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_category_delete_invalid_pk(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test1_token.key)
        response = self.client.delete(reverse("delete_category", kwargs={"pk": self.two_category.id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_category_delete_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test1_token.key)
        result = Category.objects.all()
        response = self.client.delete(reverse("delete_category", kwargs={"pk": self.one_category.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotEqual(result, Category.objects.all())

    def test_selected_category_invalid(self):
        response = self.client.get(reverse("selected_category_cards", kwargs={"pk": self.one_category.id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_selected_category_invalid_pk(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test1_token.key)
        response = self.client.get(reverse("selected_category_cards", kwargs={"pk": self.two_category.id}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["category"], "you have entered a non-existent list")

    def test_selected_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test1_token.key)
        response = self.client.get(reverse("selected_category_cards", kwargs={"pk": self.one_category.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
