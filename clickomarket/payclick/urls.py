from django.urls import path

from .views import ItemDetailsView, create_checkout_session, cancel_view

app_name = 'payclick'

urlpatterns = [
    path('payclick/<int:pk>/', ItemDetailsView.as_view(), name='item'),
    path('payclick/buy/<int:pk>/', create_checkout_session, name='create-checkout-session'),
    path('cancel/', cancel_view, name='cancel'),
]
