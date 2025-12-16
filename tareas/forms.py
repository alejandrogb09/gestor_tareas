from django import forms
from .models import Tarea, Categoria
from django.utils import timezone

class TareaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields["categoria"].queryset = Categoria.objects.filter(user=user)

    class Meta:
        model = Tarea
        fields = ["titulo", "descripcion", "fecha_vencimiento", "prioridad", "categoria", "estado"]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control", "placeholder": "Título"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Descripción"}),
            "fecha_vencimiento": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
            "prioridad": forms.Select(attrs={"class": "form-control"}),
            "categoria": forms.Select(attrs={"class": "form-control"}),
            "estado": forms.Select(attrs={"class": "form-control"}),
        }

    def clean_titulo(self):
        titulo = self.cleaned_data.get("titulo")
        if len(titulo) < 3:
            raise forms.ValidationError("El título debe tener al menos 3 caracteres.")
        return titulo
    
    def clean_fecha_vencimiento(self):
        fecha = self.cleaned_data.get("fecha_vencimiento")
        if fecha and fecha < timezone.now():
            raise forms.ValidationError("La fecha de vencimiento no puede estar en el pasado.")
        return fecha
    
    def clean_prioridad(self):
        prioridad = self.cleaned_data.get("prioridad")
        if prioridad not in ["baja", "media", "alta"]:
            raise forms.ValidationError("La prioridad no es válida.")
        return prioridad

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ["nombre"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre de la categoría"})
        }
    
    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre")

        usuario = self.instance.user or self.initial.get("user")

        if Categoria.objects.filter(nombre__iexact=nombre, user=usuario).exists():
            raise forms.ValidationError("Esta categoría ya existe.")
        
        return nombre