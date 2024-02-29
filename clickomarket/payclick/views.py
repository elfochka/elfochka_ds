import stripe
from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import DetailView

from .models import Item

stripe.api_key = settings.STRIPE_SECRET_KEY


# set :static, true
# set :port, 4242

class ItemDetailsView(DetailView):
    model = Item
    template_name = 'payclick/item.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stripe_public_key'] = settings.STRIPE_PUBLIC_KEY
        return context


def create_checkout_session(request, pk):
    item = Item.objects.get(id=pk)

    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': item.price_id,
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=request.build_absolute_uri('/') + '/success',
            cancel_url=request.build_absolute_uri('/') + '/cancel',
        )

        return redirect(checkout_session.url, code=303)
    except Exception as e:
        return JsonResponse({'error': str(e)})


def cancel_view(request):
    referer_url = request.META.get('HTTP_REFERER')

    if referer_url:
        return HttpResponseRedirect(referer_url)
    else:
        return redirect('../payclick/1/')
