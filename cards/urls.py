from django.urls import path

from .views import *


urlpatterns = [
    path('card/', CardAPIList.as_view(), name="user_cards"),
    path('card/<int:pk>/', CardAPIUpdate.as_view(), name="update_cards"),
    path('carddelete/<int:pk>/', CardAPIDestroy.as_view(), name="delete_card"),
    path('category/', CategoryAPIList.as_view(), name="user_category"),
    path('category/<int:pk>/', CategoryAPIUpdate.as_view(), name="update_category"),
    path('categorydelete/<int:pk>/', CategoryAPIDestroy.as_view(), name="delete_category"),
    path('selected_category/<int:pk>/', SelectedCategoryCardsAPIList.as_view(), name="selected_category_cards"),
]
