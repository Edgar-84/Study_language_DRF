from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

from .models import *


class AddCategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AddCategoryForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Category
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        list_titles = Category.objects.filter(user=self.request.user).values_list('title', flat=True).distinct()
        if title in list_titles:
            raise ValidationError(("У вас уже есть список с именем '%(value)s'!"),
                                  code='invalid',
                                  params={'value': title})
        return title


class AddCardForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        self.cat_id = kwargs.pop("cat_id")
        super(AddCardForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Card
        fields = ['title_native_language', 'translate_studied_language',
                  'usage_example', 'photo']
        widgets = {
            'usage_example': forms.Textarea(attrs={'cools': 60, 'rows': 10}),
        }

    def clean_title_native_language(self):
        title = self.cleaned_data['title_native_language']
        list_titles = Card.objects.filter(user=self.request.user,
                                          category=self.cat_id). \
            values_list('title_native_language', flat=True).distinct()

        if title in list_titles:
            raise ValidationError(("Карточка с именем '%(value)s' уже есть в списке!"),
                                  code='invalid',
                                  params={'value': title})
        return title


class EditCardForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        self.card_id = kwargs.pop("card_id")
        super(EditCardForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Card
        fields = ['title_native_language', 'translate_studied_language',
                  'usage_example', 'photo']
        widgets = {
            'usage_example': forms.Textarea(attrs={'cools': 60, 'rows': 10}),
        }

    def clean_title_native_language(self):
        title = self.cleaned_data['title_native_language']
        card_object = Card.objects.filter(id=self.card_id)
        for_compare_id = Card.objects.filter(title_native_language=title,
                                             category=card_object[0].category_id)
        if len(for_compare_id) == 0:
            for_compare_id = None
        else:
            for_compare_id = for_compare_id[0].id

        list_titles = Card.objects.filter(user=self.request.user,
                                          category=card_object[0].category_id). \
            values_list('title_native_language', flat=True).distinct()

        if (title in list_titles) and (self.card_id != for_compare_id):
            raise ValidationError(("Карточка с именем '%(value)s' уже есть в списке!"),
                                  code='invalid',
                                  params={'value': title})
        return title


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
