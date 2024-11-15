# listings/admin.py
from django.contrib import admin
from .models import Inmueble
# Importa el modelo Inmueble

 # Asegúrate de importar el model
@admin.register(Inmueble)
class InmuebleAdmin(admin.ModelAdmin):
    list_display = ('tipo_inmueble', 'direccion', 'precio', 'usuario', 'distancia')  # Columnas visibles en la lista de inmuebles
    search_fields = ('direccion', 'descripcion')  # Campos que puedes buscar
    list_filter = ('tipo_inmueble', 'distancia')  # Filtro