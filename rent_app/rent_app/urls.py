"""
URL configuration for rent_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# rent_app/urls.py
from django.contrib import admin
from django.urls import path, include
from listings import views
from django.conf import settings
from django.conf.urls.static import static
from listings.views import CustomLoginView, RegisterView
from django.contrib.auth.views import LogoutView 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),  # Ruta de inicio de sesión
    path('register/', RegisterView.as_view(), name='register'),  # Ruta de registro
    path('perfil/', views.perfil, name='perfil'),  # Ruta para el perfil del usuario
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),  # Ruta para editar perfil
    path('mis_inmuebles/', views.mis_inmuebles, name='mis_inmuebles'),  # Ruta para ver mis inmuebles
    path('inmueble/<int:inmueble_id>/', views.inmueble_detalle, name='inmueble_detalle'),  # Ruta para detalle de inmueble
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),  # Ruta de cierre de sesión
    path('publicar/', views.publicar_inmueble, name='publicar_inmueble'), 
     # Ruta para publicar un inmueble
]



# Configuración para servir archivos de media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)