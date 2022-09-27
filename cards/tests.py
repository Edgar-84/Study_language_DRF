from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.test.client import Client

from .models import Card, Category


class CardsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@mail.ru',
            password='unittestpassword123'
        )

        self.category = Category.objects.create(
            user=self.user,
            title='test_category',
        )

        self.card = Card.objects.create(
            user=self.user,
            category=self.category,
            title_native_language='Первое тестовое слово',
            translate_studied_language='First test word',
            usage_example='Here we will use first test word',
        )
        self.client.post(reverse('login'),
                         {'username': 'testuser',
                          'password': 'unittestpassword123'})

    def test_LoginUser(self):
        request = self.client.post(reverse('login'),
                                   {'username': 'testuser',
                                    'password': 'unittestpassword123'})
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_get_absolute_url(self):
        """Check generate unique slug"""
        self.assertEqual(self.card.get_absolute_url() in Card.objects.values_list('slug', flat=True), False)

    def test_card_content(self):
        self.assertEqual(f'{self.card.user}', 'testuser')
        self.assertEqual(f'{self.card.category}', 'test_category')
        self.assertEqual(f'{self.card.title_native_language}', 'Первое тестовое слово')
        self.assertEqual(f'{self.card.translate_studied_language}', 'First test word')
        self.assertEqual(f'{self.card.usage_example}', 'Here we will use first test word')

    def test_card_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test_category')
        self.assertTemplateUsed(response, 'cards/index.html')

    def test_card_detail_view(self):
        response = self.client.get(self.card.get_absolute_url())
        no_response = self.client.get('/post/100sdfsadf000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Первое тестовое слово')
        self.assertTemplateUsed(response, 'cards/card_info.html')

    def test_card_create_view(self):
        response = self.client.post(reverse('add_card', args=str(self.category.id)), {
            'title_native_language': 'слово',
            'translate_studied_language': 'перевод',
            'usage_example': 'слово-перевод'})

        self.assertEqual(response.status_code, 302)
        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'слово')
        self.assertContains(response, 'перевод')
        self.assertContains(response, 'слово-перевод')

    def test_card_update_view(self):
        response = self.client.post(reverse('update_card', args=str(self.card.id)),
                                    {
                                        'title_native_language': 'измененное слово',
                                        'translate_studied_language': 'измененный перевод',
                                    })
        self.assertEqual(response.status_code, 302)
        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'измененное слово')
        self.assertContains(response, 'измененный перевод')

    def test_card_add_same_card(self):
        """ checking the addition of cards with the same names """

        response = self.client.post(reverse('add_card', args=str(self.category.id)), {
            'title_native_language': 'Первое тестовое слово',
            'translate_studied_language': 'First test word',
            'usage_example': 'First word'})

        self.assertEqual(response.status_code, 200)

    def test_card_delete_view(self):
        response = self.client.post(
            reverse('delete_card', args=str(self.card.id)))
        self.assertEqual(response.status_code, 302)

    def test_category_create(self):
        response = self.client.post(reverse('add_category'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('add_category'), {
            'title': 'new category',
        })
        self.assertEqual(response.status_code, 302)

    def test_category_create_same_category(self):
        response = self.client.post(
            reverse('add_category'), {
                'title': 'test_category',
            })
        self.assertEqual(response.status_code, 200)
