# listings/views.py
from django.contrib.auth import login
from django.contrib import messages
from django.conf import settings
from django.views.generic import CreateView
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, EmailAuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import InmuebleForm, ImagenInmuebleForm
from .models import ImagenInmueble, Inmueble

def home(request):
    # Obtén los valores de los filtros desde los parámetros GET de la URL
    tipo = request.GET.get('tipo')
    costo = request.GET.get('costo')
    distancia = request.GET.get('distancia')

    # Empieza con todos los inmuebles
    inmuebles = Inmueble.objects.all()

    # Filtra según el tipo de inmueble si está presente en la URL
    if tipo:
        inmuebles = inmuebles.filter(tipo_inmueble=tipo)

    # Filtra por rango de precio si el filtro de costo está presente
    if costo:
        min_price, max_price = map(int, costo.split('-'))
        inmuebles = inmuebles.filter(precio__gte=min_price, precio__lte=max_price)

    # Filtra por distancia si está presente
    if distancia:
        inmuebles = inmuebles.filter(distancia=distancia)

    return render(request, 'home.html', {'inmuebles': inmuebles})
class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = settings.LOGIN_REDIRECT_URL

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Cuenta creada exitosamente. Por favor, inicia sesión.")
        return response

class CustomLoginView(View):
    form_class = EmailAuthenticationForm
    template_name = 'login.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.cleaned_data.get("user")
            login(request, user)
            messages.success(request, "Has iniciado sesión exitosamente.")
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            messages.error(request, "Lo sentimos, el correo y/o contraseña no coinciden, intenta de nuevo.")
            return render(request, self.template_name, {'form': form})
        
def inmueble_detalle(request, inmueble_id):
    # Usa get_object_or_404 para obtener el inmueble o mostrar 404 si no existe
    inmueble = get_object_or_404(Inmueble, id=inmueble_id)
    return render(request, 'inmueble_detalle.html', {'inmueble': inmueble})

@login_required
def perfil(request):
    return render(request, 'perfil.html', {'user': request.user})


@login_required
def editar_perfil(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado exitosamente.")
            return redirect('perfil')
    else:
        form = CustomUserCreationForm(instance=request.user)
    
    return render(request, 'editar_perfil.html', {'form': form})

@login_required
def mis_inmuebles(request):
    inmuebles = Inmueble.objects.filter(usuario=request.user)  # Filtra por usuario actual
    return render(request, 'mis_inmuebles.html', {'inmuebles': inmuebles})


@login_required
def publicar_inmueble(request):
    if request.method == 'POST':
        inmueble_form = InmuebleForm(request.POST)
        imagen_form = ImagenInmuebleForm(request.POST, request.FILES)

        if inmueble_form.is_valid() and imagen_form.is_valid():
            inmueble = inmueble_form.save(commit=False)
            inmueble.usuario = request.user
            inmueble.save()

            # Guardar cada imagen en el modelo de imágenes usando getlist
            for imagen in request.FILES.getlist('imagenes'):
                ImagenInmueble.objects.create(inmueble=inmueble, imagen=imagen)

            messages.success(request, "Inmueble publicado exitosamente.")
            return redirect('home')
    else:
        inmueble_form = InmuebleForm()
        imagen_form = ImagenInmuebleForm()

    return render(request, 'publicar_inmueble.html', {'inmueble_form': inmueble_form, 'imagen_form': imagen_form})

def inmueble_detalle(request, inmueble_id):
    # Obtén el inmueble específico usando el id proporcionado
    inmueble = get_object_or_404(Inmueble, id=inmueble_id)
    return render(request, 'inmueble_detalle.html', {'inmueble': inmueble})