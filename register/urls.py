from django.urls import path

from .views import RegisterFormView

app_name = "register"
urlpatterns = [
    path("register/", RegisterFormView.as_view(), name="register"),
]
