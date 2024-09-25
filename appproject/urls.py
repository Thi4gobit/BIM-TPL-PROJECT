from django.urls import path
from .views import *


urlpatterns = [
    
    path('field/', FieldListOrCreateView.as_view(), name='list-create-field'),
    path('field/<int:pk>/', FieldRetrieveUpdateDeleteView.as_view(), name='get-update-delete-field'),

    path('group/', GroupListOrCreateView.as_view(), name='list-create-group'),
    path('group/<int:pk>/', GroupRetrieveUpdateDeleteView.as_view(), name='get-update-delete-group'),




    # path('items/', ItemListCreateView.as_view(), name='item-detail'),
    # path('items/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),

]
