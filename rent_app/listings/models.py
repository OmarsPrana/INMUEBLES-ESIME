# listings/models.py
from django.db import models
from django.contrib.auth.models import User

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
    
# listings/models.py
from django.db import models
from django.contrib.auth.models import User

class Inmueble(models.Model):
    TIPOS_INMUEBLE = [
        ('Departamento', 'Departamento'),
        ('Casa', 'Casa'),
        ('Cuarto', 'Cuarto'),
    ]

    DISTANCIAS = [
        ('0-5 km', '0-5 km'),
        ('5-10 km', '5-10 km'),
        ('10-15 km', '10-15 km'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo_inmueble = models.CharField(max_length=50, choices=TIPOS_INMUEBLE)
    distancia = models.CharField(max_length=50, choices=DISTANCIAS)
    direccion = models.CharField(max_length=255)
    codigo_postal = models.CharField(max_length=10)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    numero_contacto = models.CharField(max_length=15)
    imagen = models.ImageField(upload_to='inmuebles/', blank=True, null=True)

    def __str__(self):
        return f"{self.tipo_inmueble} en {self.direccion}"


class ImagenInmueble(models.Model):
    inmueble = models.ForeignKey(Inmueble, related_name="imagenes", on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='inmuebles/imagenes/')

    def __str__(self):
        return f"Imagen de {self.inmueble}"