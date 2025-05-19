"""
Main URL configuration for the kelaasorPanel project.
Includes route mappings for apps like user, ticket, admin_status, bootcamps, and financial.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("user.urls")),
    path("ticket/", include("ticket.urls")),
    path("admin-status/", include("admin_status.urls")),
    path("bootcamps/", include("bootcamps.urls")),
    path("financial/", include("financial.urls")),
]
