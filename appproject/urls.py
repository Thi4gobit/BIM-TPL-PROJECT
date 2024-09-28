from django.urls import path
from .views import *


urlpatterns = [
    
    path('field/', FieldListCreateView.as_view(), name='field-list-create'),
    # path('field/<int:pk>/', FieldRetrieveUpdateDeleteView.as_view(), name='get-update-delete-field'),

    # path('group/', GroupListOrCreateView.as_view(), name='list-create-group'),
    # path('group/<int:pk>/', GroupRetrieveUpdateDeleteView.as_view(), name='get-update-delete-group'),




    # path('items/', ItemListCreateView.as_view(), name='item-detail'),
    # path('items/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),

]
