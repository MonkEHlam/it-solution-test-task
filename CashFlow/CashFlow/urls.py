from django.contrib import admin
from django.urls import path
from CashFlowRecords import views

urlpatterns = [
    path(
        "admin/get_categories/",
        views.get_categories,
        name="get_categories",
    ),
    path(
        "admin/get_subcategories/",
        views.get_subcategories,
        name="get_subcategories",
    ),
    path("", admin.site.urls),
]
