from django.urls import path
from .views import (
    AdListView, AdDetailView, AdCreateView, AdUpdateView, AdDeleteView,
    AdImageCreateView,
    FavoriteListView, FavoriteCreateView, FavoriteDeleteView,
    MessageListView, MessageCreateView,
)

urlpatterns = [
    # Ad CRUD
    path('', AdListView.as_view(), name='ad_list'),
    path('ad/<int:pk>/', AdDetailView.as_view(), name='ad_detail'),
    path('ad/create/', AdCreateView.as_view(), name='ad_create'),
    path('ad/<int:pk>/edit/', AdUpdateView.as_view(), name='ad_edit'),
    path('ad/<int:pk>/delete/', AdDeleteView.as_view(), name='ad_delete'),

    # AdImage
    path('ad/<int:ad_id>/image/upload/', AdImageCreateView.as_view(), name='ad_image_upload'),

    # Favorites
    path('favorites/', FavoriteListView.as_view(), name='favorite_list'),
    path('favorites/add/', FavoriteCreateView.as_view(), name='favorite_add'),
    path('favorites/<int:pk>/delete/', FavoriteDeleteView.as_view(), name='favorite_delete'),

    # Messages
    path('messages/', MessageListView.as_view(), name='message_list'),
    path('messages/send/', MessageCreateView.as_view(), name='message_send'),
]
