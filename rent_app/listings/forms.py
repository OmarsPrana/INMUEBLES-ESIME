# listings/forms.py
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Inmueble, ImagenInmueble

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
        fields = ['tipo_inmueble', 'distancia', 'direccion', 'codigo_postal', 'descripcion', 'precio', 'numero_contacto', 'imagen']
        widgets = {
            'tipo_inmueble': forms.Select(attrs={'class': 'form-control'}),
            'distancia': forms.Select(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_postal': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'numero_contacto': forms.TextInput(attrs={'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
        }


class ImagenInmuebleForm(forms.Form):
    imagenes = forms.FileField(widget=forms.FileInput(), label="Cargar fotos (mínimo 7, máximo 15)", required=True)

