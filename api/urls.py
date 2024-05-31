from django.urls import path
from . import views

urlpatterns = [
    path("overview/", views.apiOverview, name="api-overview"),
    path("goals/", views.goals, name="goal"),
    path("goals/<int:goal_id>", views.goal, name="goal"),
    path("goals/<int:goal_id>/tasks/", views.task, name="task"),
    path("goals/<int:goal_id>/task/<int:pk>/", views.taskDetail, name="taskdetail"),
    path("auth/reg", views.userAuthetication, name="register"),
    path("auth/login", views.userLogin, name="clogin"),
]
