# listings/models.py
from django.db import models
from django.conf import settings
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
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inmuebles')
    

    
    tipo_inmueble = models.CharField(max_length=50, choices=TIPOS_INMUEBLE)
    distancia = models.CharField(max_length=50, choices=DISTANCIAS)
    direccion = models.CharField(max_length=255)
    codigo_postal = models.CharField(max_length=10)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    numero_contacto = models.CharField(max_length=15)
    calificacion = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    arrendador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="arrendados")

    arrendatario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="alquileres")
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    


    def __str__(self):
        return f"{self.tipo_inmueble} en {self.direccion}"

class HistorialRenta(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    inmueble = models.ForeignKey(Inmueble, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)  # Puede estar vacío si el usuario aún renta
    aun_renta = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.usuario.username} - {self.inmueble}"

 

class ImagenInmueble(models.Model):
    inmueble = models.ForeignKey(Inmueble, related_name='imagenes', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='inmuebles/imagenes/')


class Calificacion(models.Model):
    inmueble = models.ForeignKey(Inmueble, related_name='calificaciones', on_delete=models.CASCADE)
    
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    aun_renta = models.BooleanField(default=False)
    
    estrellas = models.PositiveSmallIntegerField(choices=[(i, f"{i} estrellas") for i in range(1, 6)])
    comentario = models.TextField()
    verificado = False


    def save(self, *args, **kwargs):
        # Si el usuario es arrendatario del inmueble, se marca como verificado.
        if self.inmueble.arrendatario == self.usuario:
            self.verificado = True
        super().save(*args, **kwargs)
    

    def __str__(self):
        return f'{self.usuario} - {self.estrellas} estrellas' if self.usuario else f'Anónimo - {self.estrellas} estrellas'