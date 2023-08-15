from django.urls import path

from . import views

app_name = "master"

urlpatterns = [
	path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("worker/", views.worker, name="worker"),
    path("storage/", views.storage, name="storage"),
    path("reputation/", views.reputation, name="reputation"),
	path("resource/", views.resource, name="resource"),
    path("tax/", views.tax, name="tax"),
    path("about/", views.about, name="about"),
]