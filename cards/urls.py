from django.urls import path

from .views import *


urlpatterns = [
    path('card/', CardViewSet.as_view({'get': 'list', 'post': 'create'}), name='card_list'),
    path('card/<int:pk>/', CardViewSet.as_view({'get': 'retrieve', 'put': 'update',
                                                'delete': 'destroy'}), name='card_detail'),
    path('category/', CategoryViewSet.as_view({'get': 'list', 'post': 'create'}), name='category_list'),
    path('category/<int:pk>/', CategoryViewSet.as_view({'get': 'retrieve', 'put': 'update',
                                                        'delete': 'destroy'}), name='category_detail'),
    path('selected_category/<int:pk>/', SelectedCategoryViewSet.as_view({'get': 'list'}), name='selected_category'),
]
