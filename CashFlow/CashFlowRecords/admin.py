from CashFlowRecords.models import CashFlowRecord, Status, Type, Category, Subcategory
from django.contrib import admin
from django import forms


def disable_related_actions(form, *fields):
    """Disable the ability to add, change, and delete instances of a related model to avoid matching errors."""
    for field_name in fields:
        if field_name in form.base_fields:
            field = form.base_fields[field_name]
            if hasattr(field, "widget"):
                if hasattr(field.widget, "can_add_related"):
                    field.widget.can_add_related = False
                if hasattr(field.widget, "can_change_related"):
                    field.widget.can_change_related = False
                if hasattr(field.widget, "can_delete_related"):
                    field.widget.can_delete_related = False
    return form


class CashFlowForm(forms.ModelForm):
    """The form is needed to clean up related models to avoid matching errors."""

    class Meta:
        model = CashFlowRecord
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "type" in self.data:
            try:
                type_id = int(self.data.get("type"))
                self.fields["category"].queryset = Category.objects.filter(
                    type_id=type_id
                )
            except (ValueError, TypeError):
                pass
        else:
            self.fields["category"].queryset = Category.objects.none()

        if "category" in self.data:
            try:
                category_id = int(self.data.get("category"))
                self.fields["subcategory"].queryset = Subcategory.objects.filter(
                    category_id=category_id
                )
            except (ValueError, TypeError):
                pass
        else:
            self.fields["subcategory"].queryset = Subcategory.objects.none()


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "type")
    list_filter = ("type",)
    search_fields = ("name",)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return disable_related_actions(form, "type")


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "get_type")
    list_filter = ("category__type", "category")
    search_fields = ("name",)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return disable_related_actions(form, "category")

    def get_type(self, obj):
        return obj.category.type

    get_type.short_description = "Type"


@admin.register(CashFlowRecord)
class CashFlowAdmin(admin.ModelAdmin):
    class Media:
        js = ("admin/js/dynamicFilter.js",)

    form = CashFlowForm
    list_display = ("datestamp", "amount", "status", "type", "category", "subcategory")
    list_filter = ("status", "type", "category", "subcategory", "datestamp")
    search_fields = ("comment", "amount")
    date_hierarchy = "datestamp"
    fieldsets = (
        (None, {"fields": ("datestamp", "status", "type", "category", "subcategory")}),
        ("Financial Data", {"fields": ("amount", "comment")}),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return disable_related_actions(
            form, "status", "type", "category", "subcategory"
        )
