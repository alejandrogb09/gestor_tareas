from django.shortcuts import redirect, get_object_or_404, render
from .models import Tarea, Categoria
from .forms import TareaForm, CategoriaForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.views.decorators.http import require_POST

class ListaTareasView(LoginRequiredMixin, ListView):
    model = Tarea
    template_name = "tareas/lista.html"
    context_object_name = "tareas"
    paginate_by = 10

    def get_queryset(self):
        queryset = Tarea.objects.filter(user=self.request.user).order_by("-fecha_creacion")

        # 1. Búsqueda
        q = self.request.GET.get("q")
        if q:
            queryset = queryset.filter(titulo__icontains=q)
        
        # 2. Filtrar por estado
        estado = self.request.GET.get("estado")
        if estado and estado != "todos":
            queryset = queryset.filter(estado=estado)

        # 3. Filtrar por prioridad
        prioridad = self.request.GET.get("prioridad")
        if prioridad and prioridad != "todas":
            queryset = queryset.filter(prioridad=prioridad)

        # 4. Filtrar por categoría
        categoria = self.request.GET.get("categoria")
        if categoria and categoria != "todas":
            queryset = queryset.filter(categoria_id=categoria)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categorias"] = Categoria.objects.all()
        return context

class CrearTareaView(LoginRequiredMixin, CreateView):
    model = Tarea
    form_class = TareaForm
    template_name = "tareas/crear.html"
    success_url = reverse_lazy("lista")

    def get_initial(self):
        initial = super().get_initial()

        # Restaurar datos enviados por GET
        for key in ["titulo", "descripcion", "fecha_vencimiento", "prioridad", "estado", "categoria"]:
            valor = self.request.GET.get(key)
            if valor:
                initial[key] = valor

        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Tarea creada correctamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Corrige los errores en el formulario.")
        return super().form_invalid(form)

class EditarTareaView(LoginRequiredMixin, UpdateView):
    model = Tarea
    form_class = TareaForm
    template_name = "tareas/editar.html"
    success_url = reverse_lazy("lista")

    def get_queryset(self):
        return Tarea.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Tarea actualizada correctamente.")
        return super().form_valid(form)    
    
    def form_invalid(self, form):
        messages.error(self.request, "Corrige los errores en el formulario.")
        return super().form_invalid(form)

class EliminarTareaView(LoginRequiredMixin, DeleteView):
    model = Tarea
    template_name = "tareas/eliminar.html"
    success_url = reverse_lazy("lista")

    def get_queryset(self):
        return Tarea.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Tarea eliminada.")
        return super().delete(request, *args, **kwargs)


class DetalleTareaView(LoginRequiredMixin, DetailView):
    model = Tarea
    template_name = "tareas/detalle.html"
    context_object_name = "tarea"

    def get_queryset(self):
        return Tarea.objects.filter(user=self.request.user)
    
@login_required
def toggle_completada(request, pk):
    tarea = get_object_or_404(Tarea, pk=pk, user=request.user)
    
    if tarea.estado == "pendiente":
        tarea.estado = "completada"
    else:
        tarea.estado = "pendiente"
    
    tarea.save()

    messages.success(request, "Estado actualizado.")    
    return redirect('lista')

class CategoriaListView(LoginRequiredMixin, ListView):
    model = Categoria
    template_name = "tareas/categorias.html"
    context_object_name = "categorias"

    def get_queryset(self):
        return Categoria.objects.filter(user=self.request.user)

from urllib.parse import urlencode

class CategoriaCreateView(LoginRequiredMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = "tareas/crear_categoria.html"
    success_url = reverse_lazy("categorias")

    def form_valid(self, form):
        # Asignar usuario antes de guardar
        form.instance.user = self.request.user
        nueva_categoria = form.save()

        # Si viene desde crear tarea, reconstruimos los datos
        if self.request.POST.get("from") == "crear":
            datos = {
                "titulo": self.request.POST.get("titulo", ""),
                "descripcion": self.request.POST.get("descripcion", ""),
                "fecha_vencimiento": self.request.POST.get("fecha_vencimiento", ""),
                "prioridad": self.request.POST.get("prioridad", ""),
                "estado": self.request.POST.get("estado", ""),
                "categoria": nueva_categoria.id,   # Seleccionar automáticamente
            }

            url = reverse("crear") + "?" + urlencode(datos)
            return redirect(url)

        messages.success(self.request, "Categoría creada correctamente.")
        return redirect("categorias")
    
def registro(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('lista')
    else:
        form = UserCreationForm()

    return render(request, "auth/registro.html", {"form": form})

@require_POST
def logout_view(request):
    logout(request)
    return redirect("login")