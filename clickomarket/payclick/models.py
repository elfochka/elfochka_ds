import stripe
from django.db import models


class Item(models.Model):
    """ Модель Item (Товар) с полями (name, description, price)."""
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()  # cents
    image = models.ImageField(upload_to='products/', blank=True, null=True)  # Новое поле
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')

    def __str__(self):
        return self.name

    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)


class Discount(models.Model):
    amount = models.IntegerField()
    description = models.TextField()


class Tax(models.Model):
    amount = models.IntegerField()
    description = models.TextField()


class Order(models.Model):
    items = models.ManyToManyField(Item)
    total_amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, blank=True, null=True)
    tax = models.ForeignKey(Tax, on_delete=models.SET_NULL, blank=True, null=True)

    def calculate_total_amount(self):
        total_amount = sum(item.price for item in self.items.all())
        if self.discount:
            total_amount -= self.discount.amount
        if self.tax:
            total_amount += self.tax.amount
        return total_amount

    def create_payment_intent(self):
        total_amount = self.calculate_total_amount()
        intent = stripe.PaymentIntent.create(
            amount=total_amount,
            currency='usd',  # Установка валюты в долларах (USD)
        )
        return intent
