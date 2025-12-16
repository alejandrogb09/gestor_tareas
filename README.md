# Gestor de Tareas – Django Web App

Aplicación web para gestionar tareas personales con autenticación de usuarios, categorías y panel de control.

## 🚀 Demo
🔗 https://gestor-tareas-x1pm.onrender.com

## 🖼️ Screenshots
![Login](screenshots/login.png)
![Registro](screenshots/registro.png)
![Lista de Tareas](screenshots/lista_tareas.png)
![Crear Tarea](screenshots/crear_tarea.png)
![Editar Tarea](screenshots/editar_tarea.png)
![Eliminar Tarea](screenshots/eliminar_tarea.png)
![Ver Detalle de Tarea](screenshots/ver_tarea.png)
![Ver Categorías](screenshots/ver_categorias.png)
![Crear Categoría](screenshots/crear_categoria.png)
![Dashboard](screenshots/dashboard.png)
![Gráfica 1](screenshots/chart_01.png)
![Gráfica 2](screenshots/chart_02.png)

## ⚙️ Funcionalidades
- Registro e inicio de sesión de usuarios
- CRUD de tareas
- Gestión de categorías
- Panel de control (dashboard)
- Mensajes de confirmación y validaciones
- Autorización por usuario (cada usuario ve solo sus datos)

## 🛠️ Tecnologías usadas
- Python 3.14.0
- Django: backend y lógica del sistema
- HTML5 / CSS3
- Bootstrap: estilos rápidos y responsivos
- PostgreSQL (Render): base de datos en producción
- Git & GitHub: control de versiones
- Render (deploy): despliegue continuo desde GitHub

## 🧠 Explicación técnica
El proyecto está estructurado siguiendo la arquitectura estándar de Django.

Se separaron las vistas de lógica general (views.py) y vistas específicas del dashboard (views_dashboard.py) para mejorar mantenibilidad.

El sistema de autenticación usa el modelo User de Django, relacionando las tareas y categorías mediante claves foráneas, garantizando aislamiento de datos por usuario.

La aplicación se desplegó en Render usando PostgreSQL como base de datos para asegurar persistencia en producción.

## 📦 Instalación local
(pasos claros)

## 👤 Autor
Alejandro Gómez Berrio — Estudiante | Backend Junior