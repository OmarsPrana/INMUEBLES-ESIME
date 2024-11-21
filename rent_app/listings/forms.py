# listings/forms.py
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Inmueble, ImagenInmueble, Calificacion



class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label="Nombre y Apellido", max_length=150, required=True)
    email = forms.EmailField(label="Correo electrónico", required=True)

    class Meta:
        model = User
        fields = ("first_name", "email", "username", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class EmailAuthenticationForm(forms.Form):
    email = forms.EmailField(label="Correo electrónico")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        
        # Buscar al usuario por correo electrónico
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError("Correo electrónico y/o contraseña incorrectos.")
        
        # Autenticar usando el nombre de usuario del usuario encontrado
        user = authenticate(username=user.username, password=password)
        
        if user is None:
            raise forms.ValidationError("Correo electrónico y/o contraseña incorrectos.")
        
        self.cleaned_data["user"] = user
        return self.cleaned_data


class InmuebleForm(forms.ModelForm):
    class Meta:
        model = Inmueble
        fields = ['tipo_inmueble', 'distancia', 'direccion', 'codigo_postal', 'descripcion', 'precio', 'numero_contacto']
        widgets = {
            'tipo_inmueble': forms.Select(attrs={'class': 'form-control'}),
            'distancia': forms.Select(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_postal': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'numero_contacto': forms.TextInput(attrs={'class': 'form-control'}),
        }


class AsignarArrendatarioForm(forms.ModelForm):
    arrendatario = forms.ModelChoiceField(queryset=User.objects.all(), required=True, label="Selecciona al arrendatario")

    class Meta:
        model = Inmueble
        fields = ['arrendatario']

class CalificacionForm(forms.ModelForm):
    class Meta:
        model = Calificacion
        fields = ['fecha_inicio', 'fecha_fin', 'aun_renta', 'estrellas', 'comentario']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Selecciona la fecha de inicio'
            }),
            'fecha_fin': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Selecciona la fecha de fin'
            }),
            'aun_renta': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'style': 'margin-top: 10px;'
            }),
            'estrellas': forms.RadioSelect(choices=[
                (1, '1 estrella'),
                (2, '2 estrellas'),
                (3, '3 estrellas'),
                (4, '4 estrellas'),
                (5, '5 estrellas')
            ], attrs={
                'class': 'form-check-inline'
            }),
            'comentario': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Escribe tu comentario...',
                'style': 'resize: none;'
            }),
        }
        labels = {
            'fecha_inicio': 'Fecha de inicio de renta',
            'fecha_fin': 'Fecha de término de renta',
            'aun_renta': '¿Aún rentas este lugar?',
            'estrellas': 'Valora este inmueble',
            'comentario': 'Agrega un comentario',
        }

    def __init__(self, *args, **kwargs):
        super(CalificacionForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'

class CalificacionForm(forms.ModelForm):
    class Meta:
        model = Calificacion
        fields = ['fecha_inicio', 'fecha_fin', 'aun_renta', 'estrellas', 'comentario']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
            'comentario': forms.Textarea(attrs={'placeholder': 'Escribe tu comentario...'}),
        }
class ReservaForm(forms.Form):
    nombre = forms.CharField(label='Nombre', max_length=100, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    apellido = forms.CharField(label='Apellido', max_length=100, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    nombre_usuario = forms.CharField(label='Nombre de Usuario', max_length=100, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    fecha_entrada = forms.DateField(label='Fecha de Entrada', widget=forms.SelectDateWidget())
    fecha_salida = forms.DateField(label='Fecha de Salida', widget=forms.SelectDateWidget())
    numero_personas = forms.IntegerField(label='Número de Personas', min_value=1)
    comentarios = forms.CharField(label='Comentarios', widget=forms.Textarea, required=False)


