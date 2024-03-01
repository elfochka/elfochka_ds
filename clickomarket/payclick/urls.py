from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import \
    ItemDetailsView, \
    SuccessView, \
    CreateCheckoutSessionView, \
    CancelView, \
    ItemListView

app_name = 'payclick'

urlpatterns = [
    path('', ItemListView.as_view(), name='catalog'),
    path('item/<int:pk>/', ItemDetailsView.as_view(), name='item'),
    path('success/', SuccessView.as_view(), name='success'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('buy/<int:pk>/', CreateCheckoutSessionView.as_view(), name='buy'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
