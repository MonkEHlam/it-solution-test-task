from django.http import JsonResponse
from .models import Category, Subcategory


def get_categories(request):
    """Returns all categories with the appropriate type. Used for AJAX"""
    type_id = request.GET.get("type__id__exact")
    categories = Category.objects.filter(type_id=type_id).values("id", "name")
    return JsonResponse(list(categories), safe=False)


def get_subcategories(request):
    """Returns all subcategories with the appropriate category. Used for AJAX."""
    category_id = request.GET.get("category__id__exact")
    subcategories = Subcategory.objects.filter(category_id=category_id).values(
        "id", "name"
    )
    return JsonResponse(list(subcategories), safe=False)
