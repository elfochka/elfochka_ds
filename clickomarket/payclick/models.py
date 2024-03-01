from django.db import models


class Item(models.Model):
    """ Модель Item (Товар) с полями (name, description, price)."""

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()  # cents
    image = models.ImageField(upload_to='products/', blank=True, null=True)  # Новое поле

    def __str__(self):
        return self.name

    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)
