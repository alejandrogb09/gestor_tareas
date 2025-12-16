from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nombre
    
class Tarea(models.Model):
    PRIORIDADES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
    ]

    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('completada', 'Completada'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_vencimiento = models.DateTimeField(null=True, blank=True)
    prioridad = models.CharField(max_length=10, choices=PRIORIDADES, default='media')
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    estado = models.CharField(max_length=12, choices=ESTADOS, default='pendiente', blank=True, null=True)

    def clean(self):
        # validar fecha
        if self.fecha_vencimiento and self.fecha_vencimiento < timezone.now():
            raise ValidationError("La fecha de vencimiento no puede ser pasada")
        
        # prioridad valida
        if self.prioridad not in ["baja", "media", "alta"]:
            raise ValidationError("La prioridad seleccionada no existe.")
        
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


    def __str__(self):
        return self.titulo
    
    # def clean(self):
    #     super().clean()

    #     if self.categoria and self.categoria.user != self.user:
    #         raise ValidationError("Categoría inválida para este usuario")