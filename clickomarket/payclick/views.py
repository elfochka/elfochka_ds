import stripe
from django.conf import settings
from django.http import JsonResponse, HttpRequest
from django.views import View
from django.views.generic import DetailView, TemplateView, ListView

from .models import Item

stripe.api_key = settings.STRIPE_SECRET_KEY


def get_full_domain(request: HttpRequest) -> str:
    """Возвращает полный домен, включая схему (http/https)."""
    scheme = request.scheme
    host = request.get_host()
    return f"{scheme}://{host}"


class ItemListView(ListView):
    template_name = 'payclick/catalog.html'
    model = Item
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        context = super(ItemListView, self).get_context_data(**kwargs)
        context['MEDIA_URL'] = settings.MEDIA_URL

        return context


class ItemDetailsView(DetailView):
    model = Item
    template_name = 'payclick/item.html'
    context_object_name = "item"

    def get_context_data(self, **kwargs):
        context = super(ItemDetailsView, self).get_context_data(**kwargs)
        context["STRIPE_PUBLIC_KEY"] = settings.STRIPE_PUBLIC_KEY
        context['MEDIA_URL'] = settings.MEDIA_URL

        return context


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        product_id = self.kwargs["pk"]
        item = Item.objects.get(id=product_id)

        request.session['previous_page'] = request.build_absolute_uri()

        YOUR_DOMAIN = get_full_domain(request)

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': item.price,
                        'product_data': {
                            'name': item.name
                        },
                    },
                    'quantity': 1,
                },
            ],
            metadata={
                "product_id": item.id
            },
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })


class SuccessView(TemplateView):
    template_name = "payclick/success.html"


class CancelView(TemplateView):
    template_name = "payclick/cancel.html"
