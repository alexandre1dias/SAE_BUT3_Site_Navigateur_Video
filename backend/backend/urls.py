from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("api-auth/", include("rest_framework.urls")), # Il n'y a pas de user Django
    path("api/", include("API.urls")),
]
