from django.urls import path

from . import views

urlpatterns = [
    path("", views.create, name="po-create"),
    path("<str:ref>/", views.detail, name="po-detail"),
]
