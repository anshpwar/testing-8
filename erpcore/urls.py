from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("inventory/", include("inventory.urls")),
    path("purchasing/", include("purchasing.urls")),
    path("entries/", include("stockmoves.urls")),
]
