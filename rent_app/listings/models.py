# listings/models.py
from django.db import models

class Listing(models.Model):
    PROPERTY_TYPES = [
        ('APARTMENT', 'Apartamento'),
        ('HOUSE', 'Casa'),
        ('ROOM', 'Cuarto'),
    ]
    
    title = models.CharField(max_length=100)
    property_type = models.CharField(max_length=10, choices=PROPERTY_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    distance = models.DecimalField(max_digits=5, decimal_places=1)
    image = models.ImageField(upload_to='listings/')

    def __str__(self):
        return self.title
