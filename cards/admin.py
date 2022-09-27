from django.contrib import admin
from .models import Card, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'time_create', 'time_update')
    list_filter = ('user',)
    search_fields = ('user',)
    prepopulated_fields = {'slug': ('title', 'user')}


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'category', 'title_native_language', 'translate_studied_language',
                    'usage_example', 'photo', 'time_create', 'time_update', 'published')
    list_display_links = ('id', 'user')
    list_filter = ('user', 'category', 'published')
    search_fields = ('user', 'category', 'title_native_language')
    raw_id_fields = ('user',)
    date_hierarchy = 'time_create'
    ordering = ('published',)
    list_editable = ('published',)
    prepopulated_fields = {'slug': ('title_native_language', 'user')}
