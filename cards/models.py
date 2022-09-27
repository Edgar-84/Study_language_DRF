from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from slugify import slugify
from time import time


class Category(models.Model):
    user = models.ForeignKey(User, related_name="category_created", on_delete=models.CASCADE)
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, db_index=True, verbose_name="URL", null=False, unique=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        unix_timestamp = str(time()).split('.')
        self.slug = '-'.join((slugify(self.title),
                              slugify(str(self.user.username)),
                              slugify(unix_timestamp[0] + unix_timestamp[1])))

        return super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['-time_update']


class Card(models.Model):
    user = models.ForeignKey(User, related_name="cards_created", on_delete=models.CASCADE, blank=True)
    category = models.ForeignKey(Category, verbose_name="category",
                                 related_name="category_created", on_delete=models.CASCADE)
    title_native_language = models.CharField(max_length=255)
    translate_studied_language = models.CharField(max_length=255)
    usage_example = models.TextField(blank=True)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True)
    slug = models.SlugField(max_length=255, db_index=True, verbose_name="URL", null=False, unique=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=True)

    def __str__(self):
        return self.title_native_language

    def save(self, *args, **kwargs):
        unix_timestamp = str(time()).split('.')
        self.slug = '-'.join((slugify(str(self.user.username)),
                              slugify(self.title_native_language),
                              slugify(str(self.category)),
                              slugify(unix_timestamp[0] + unix_timestamp[1])))

        return super(Card, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('card', kwargs={'card_slug': self.slug})

    class Meta:
        verbose_name = "Card"
        verbose_name_plural = "Cards"
        ordering = ['time_create', 'title_native_language']
