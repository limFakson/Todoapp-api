from django.urls import path
from . import views

urlpatterns = [
    path("overview/", views.apiOverview, name="api-overview"),
    path("goal/", views.goals, name="goal"),
    path("goal/<int:pk>", views.goal, name="goal"),
    path("goal/<int:goal_id>/task/", views.task, name="task"),
    path("goal/<int:goal_id>/task/<int:pk>/", views.taskDetail, name="taskdetail"),
    path("auth/reg", views.userAuthetication, name="register"),
    path("auth/login", views.userLogin, name="clogin"),
    path("", views.userId, name="get-id"),
]
