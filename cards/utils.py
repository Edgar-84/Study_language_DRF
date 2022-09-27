from .models import *

menu = [{"title": "Главная", "url_name": "home"},
        {"title": "О сайте", "url_name": "about"},
        {"title": "Начать занятие", "url_name": "show_menu"},
        {"title": "Обратная связь", "url_name": "contact"},
        ]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        if self.request.user.is_authenticated:
            cats = Category.objects.filter(user=self.request.user)
        else:
            cats = Category.objects.all()
        context['menu'] = menu
        context['cats'] = cats
        return context
