from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Tarea
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import TruncDate

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        total_tareas = Tarea.objects.filter(user=user).count()
        tareas_completadas = Tarea.objects.filter(user=user, estado="completada").count()
        tareas_pendientes = Tarea.objects.filter(user=user, estado="pendiente").count()

        prioridades = (
            Tarea.objects
            .filter(user=user)
            .values("prioridad")
            .annotate(total=Count("id"))
        )

        context["total_tareas"] = total_tareas
        context["tareas_completadas"] = tareas_completadas
        context["tareas_pendientes"] = tareas_pendientes
        context["prioridades"] = prioridades

        total_tareas = Tarea.objects.filter(user=user).count()
        tareas_completadas = Tarea.objects.filter(
            user = user, estado="completada"
        ).count()

        porcentaje_completadas = 0
        if total_tareas > 0:
            porcentaje_completadas = round(
                (tareas_completadas / total_tareas) * 100, 1
            )

        context["porcentaje_completadas"] = porcentaje_completadas

        hace_7_dias = timezone.now() - timedelta(days=7)

        productividad_semanal = Tarea.objects.filter(
            user=user,
            estado="completada",
            fecha_creacion__gte=hace_7_dias
        ).count()

        context["productividad_semanal"] = productividad_semanal

        tareas_vencidas = Tarea.objects.filter(
            user=user,
            estado="pendiente",
            fecha_vencimiento__lt=timezone.now()
        ).count()

        context["tareas_vencidas"] = tareas_vencidas

        if porcentaje_completadas >= 80:
            badge = "Excelente"
        elif porcentaje_completadas >= 50:
            badge = "Buen progreso"
        else:
            badge = "Necesita enfoque"

        context["badge"] = badge

        labels = []
        data = []

        for p in prioridades:
            labels.append(p["prioridad"])
            data.append(p["total"])

        context["chart_labels"] = labels
        context["chart_data"] = data

        productividad_diaria = (
            Tarea.objects
            .filter(
                user=user,
                estado="completada",
                fecha_creacion__gte=hace_7_dias
            )
            .annotate(dia=TruncDate("fecha_creacion"))
            .values("dia")
            .annotate(total=Count("id"))
            .order_by("dia")
        )

        labels_prod = []
        data_prod = []

        for item in productividad_diaria:
            labels_prod.append(item["dia"].strftime("%d %b"))
            data_prod.append(item["total"])

        context["prod_labels"] = labels_prod
        context["prod_data"] = data_prod


        mensaje_productividad = "Sin datos suficientes"

        if len(data_prod) >= 2:
            if data_prod[-1] > data_prod[0]:
                mensaje_productividad = "Vas mejorando esta semana 🚀"
            elif data_prod[-1] < data_prod[0]:
                mensaje_productividad = "Tu productividad bajó, ojo 👀"
            else:
                mensaje_productividad = "Te mantuviste estable"

        context["mensaje_productividad"] = mensaje_productividad

        return context