from django.urls import path
from .views import *


urlpatterns = [
    path('group/', GroupFieldListCreateView.as_view(), name='post-list-create'),
    path('group/<int:pk>/', GroupFieldDetailView.as_view(), name='post-detail'),

    path('field/', FieldListCreateView.as_view(), name='list-or-create-many-field'),
    path('field/<int:pk>/', FieldDetailView.as_view(), name='post-detail'),

    path('field-compose/', FieldRelationshipListView.as_view(), name='post-list-field-relationship'),
    path('field-compose/update', FieldRelationshipUpdateListView.as_view(), name='update-list-field-relationship'),
    #path('field-compose/', FieldRelationshipCreateView.as_view(), name='post-list-field-relationship'),

    path('items/', ItemListCreateView.as_view(), name='item-detail'),
    path('items/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
]
