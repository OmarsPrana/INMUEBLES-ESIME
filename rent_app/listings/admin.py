# listings/admin.py
from django.contrib import admin
from .models import Inmueble,Reserva
# Importa el modelo Inmueble
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'inmueble', 'estado_pago', 'fecha_reserva')  # Campos que se mostrarán en la lista
    search_fields = ('usuario__username', 'inmueble__nombre')  # Campos que se podrán buscar
    list_filter = ('estado_pago', 'fecha_reserva')  # Filtros para facilitar la búsqueda

# Registrar el modelo Reserva con la clase de configuración ReservaAdmin
admin.site.register(Reserva, ReservaAdmin)
 # Asegúrate de importar el model
@admin.register(Inmueble)
class InmuebleAdmin(admin.ModelAdmin):
    list_display = ('tipo_inmueble', 'direccion', 'precio', 'usuario', 'distancia')  # Columnas visibles en la lista de inmuebles
    search_fields = ('estado','direccion', 'descripcion')  # Campos que puedes buscar
    list_filter = ('tipo_inmueble', 'distancia')  # Filtro

