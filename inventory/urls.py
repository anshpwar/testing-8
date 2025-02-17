from django.urls import path

from . import views

urlpatterns = [
    path("valuation/", views.valuation_report, name="valuation"),
    path("aging/", views.aging_report, name="aging"),
]
