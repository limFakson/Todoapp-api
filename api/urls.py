from django.urls import path
from . import views

urlpatterns = [
    path("overview/", views.apiOverview, name="api-overview"),
    path("task/", views.task, name="task"),
    path("task/<int:pk>/", views.taskDetail, name="taskdetail"),
    path("auth/", views.userAuthetication, name="authentication"),
]
