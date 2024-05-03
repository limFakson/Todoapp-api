from django.urls import path
from . import views

urlpatterns = [
    path("overview/", views.apiOverview, name="api-overview"),
    path("task/", views.task, name="task"),
    path("task/<int:pk>/", views.taskDetail, name="taskdetail"),
    path("auth/reg", views.userAuthetication, name="register"),
    path("auth/login", views.userLogin, name="clogin"),
]
