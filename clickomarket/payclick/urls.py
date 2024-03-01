from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import (CancelView, CreateCheckoutSessionView, ItemDetailsView,
                    ItemListView, OrderDetailsView, OrderListView,
                    StripeIntentView, SuccessView, UpdateOrderPayment)

app_name = 'payclick'

urlpatterns = [
    path('', ItemListView.as_view(), name='catalog'),
    path('item/<int:pk>/', ItemDetailsView.as_view(), name='item'),
    path('success/', SuccessView.as_view(), name='success'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('buy/<int:pk>/', CreateCheckoutSessionView.as_view(), name='buy'),
    path('orders/', OrderListView.as_view(), name='orders'),
    path('order/<int:pk>/', OrderDetailsView.as_view(), name='order'),
    path('order_pay/<int:pk>/', StripeIntentView.as_view(), name='order_pay'),
    path('update_order_payment/', UpdateOrderPayment.as_view(), name='update_order_payment'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
