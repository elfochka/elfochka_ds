from django.db import models


class Item(models.Model):
    """ Модель Item (Товар) с полями (name, description, price)."""

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    price_id = models.CharField(max_length=50)

    def __str__(self):
        return self.name
