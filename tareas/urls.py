from django.urls import path
from .views_dashboard import DashboardView
from .views import (
    ListaTareasView, CrearTareaView, EditarTareaView,
    EliminarTareaView, DetalleTareaView, toggle_completada,
    CategoriaListView, CategoriaCreateView, registro
)

urlpatterns = [
    path('', ListaTareasView.as_view(), name='lista'),
    path('crear/', CrearTareaView.as_view(), name='crear'),
    path('editar/<int:pk>/', EditarTareaView.as_view(), name='editar'),
    path('eliminar/<int:pk>/', EliminarTareaView.as_view(), name='eliminar'),
    path('detalle/<int:pk>/', DetalleTareaView.as_view(), name='detalle'),
    path('toggle/<int:pk>/', toggle_completada, name='toggle_completada'),
    path('categorias/', CategoriaListView.as_view(), name='categorias'),
    path('categorias/crear/', CategoriaCreateView.as_view(), name='crear_categoria'),
    path('dashboard/', DashboardView.as_view(), name="dashboard"),
]