import stripe
from django.db import models


class Item(models.Model):
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()  # cents
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')

    def __str__(self):
        return f"{self.name} id: {self.pk}"

    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)


class Discount(models.Model):
    amount = models.IntegerField()
    description = models.TextField()


class Tax(models.Model):
    amount = models.IntegerField()
    description = models.TextField()


class Order(models.Model):
    items = models.ManyToManyField(Item, related_name='order', verbose_name='Товары в заказе')
    created_at = models.DateTimeField(auto_now_add=True)
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, blank=True, null=True)
    tax = models.ForeignKey(Tax, on_delete=models.SET_NULL, blank=True, null=True)
    stripe_payment_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='ID платежа в Stripe')

    def __str__(self):
        return f"Заказ № {self.pk} от {self.created_at}"

    def total_amount(self):
        total_amount = sum(item.price for item in self.items.all())
        if self.discount:
            total_amount -= self.discount.amount
        if self.tax:
            total_amount += self.tax.amount

        return total_amount

    def get_display_total_amount(self):
        return "{0:.2f}".format(self.total_amount() / 100)

    def get_stripe_payment_status(self):
        if self.stripe_payment_id:
            data = stripe.PaymentIntent.retrieve(self.stripe_payment_id)
            stripe_payment_id = data['status']
            return stripe_payment_id
        else:
            return None
