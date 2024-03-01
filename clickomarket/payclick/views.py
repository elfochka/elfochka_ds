import json

import stripe
from django.conf import settings
from django.http import JsonResponse, HttpRequest
from django.views import View
from django.views.generic import DetailView, TemplateView, ListView, CreateView, DeleteView

from .models import Item, Order

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.SetupIntent.create(usage="on_session")


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

        your_domain = get_full_domain(request)

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': item.currency,
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
            success_url=your_domain + '/success/',
            cancel_url=your_domain + '/cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })


class SuccessView(TemplateView):
    template_name = "payclick/success.html"


class CancelView(TemplateView):
    template_name = "payclick/cancel.html"


class OrderListView(ListView):
    model = Order
    template_name = 'payclick/order_list.html'
    context_object_name = 'orders'


class OrderDetailsView(DetailView):
    queryset = (
        Order.objects.prefetch_related('items')
    )
    template_name = 'payclick/order.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super(OrderDetailsView, self).get_context_data(**kwargs)
        context["STRIPE_PUBLIC_KEY"] = settings.STRIPE_PUBLIC_KEY

        return context


class StripeIntentView(View):
    def post(self, request, *args, **kwargs):
        try:
            req_json = json.loads(request.body)
            customer = stripe.Customer.create(email=req_json['email'])
            order = Order.objects.get(id=self.kwargs["pk"])
            intent = stripe.PaymentIntent.create(
                amount=order.total_amount(),
                currency='usd',
                customer=customer['id'],
                metadata={
                    "order_id": order.id
                },
            )
            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        except Exception as e:
            return JsonResponse({'error': str(e)})


class UpdateOrderPayment(View):
    def post(self, request):
        if request.method == "POST":
            data = json.loads(request.body)
            order_id = data.get('order_id')
            stripe_payment_id = data.get('stripe_payment_id')

            print(data)

            try:
                order = Order.objects.get(pk=order_id)
                order.stripe_payment_id = stripe_payment_id
                order.save()
                return JsonResponse({"message": "Payment ID updated successfully."})
            except Order.DoesNotExist:
                return JsonResponse({"error": "Order not found."}, status=404)

        return JsonResponse({"error": "Invalid request"}, status=400)
