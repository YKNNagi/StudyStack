from django.urls import path
from . import views

urlpatterns = [
    path("",views.index, name="index"),
    path("signup/",views.signup, name="signup"),
    path("login/",views.login_view,name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("update/<int:study_id>/",views.update_view,name="update"),
    path("delete/<int:study_id>/",views.delete_view,name="delete"),
    path("logout/",views.logout_view,name = "logout"),
]