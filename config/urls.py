from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from tareas.views import registro
from tareas.views import logout_view

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('registro/', registro, name='registro'),

    path('', include("tareas.urls")),
]