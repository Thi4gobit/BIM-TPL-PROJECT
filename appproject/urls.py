from django.urls import path
from .views import *

urlpatterns = [
    path('group/', GroupFieldListCreateView.as_view(), name='post-list-create'),
    path('group/<int:pk>/', GroupFieldDetailView.as_view(), name='post-detail'),

    path('field/', FieldListCreateView.as_view(), name='post-list-create'),
    path('field/<int:pk>/', FieldDetailView.as_view(), name='post-detail'),

    path('field-compose/', FieldSelfRelationshipCreateView.as_view(), name='post-list-create'),

    path('items/', ItemListCreateView.as_view(), name='item-detail'),
    path('items/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
]
