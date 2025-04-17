from django.db import models


MAXCHARINNAME = 40  # Just a simple constant


class Type(models.Model):
    """Represents the type of records."""

    name = models.CharField(max_length=MAXCHARINNAME, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "type"
        verbose_name_plural = "types"


class Category(models.Model):
    """Represents the category of records."""

    name = models.CharField(max_length=MAXCHARINNAME, unique=True)
    type = models.ForeignKey(
        Type, on_delete=models.CASCADE, related_name="categories", verbose_name="type"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
        unique_together = ("type", "name")


class Subcategory(models.Model):
    """Represents the subcategory of records."""

    name = models.CharField(max_length=MAXCHARINNAME, unique=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="subcategories",
        verbose_name="category",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "subcategory"
        verbose_name_plural = "subcategories"
        unique_together = ("category", "name")


class Status(models.Model):
    """Represents the status of records."""

    name = models.CharField(max_length=MAXCHARINNAME, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "status"
        verbose_name_plural = "statuses"


class CashFlowRecord(models.Model):
    """Represents a cash flow record."""

    datestamp = models.fields.DateField()
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    type = models.ForeignKey(Type, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.PROTECT)
    amount = models.FloatField()
    comment = models.TextField(blank=True, default="")

    def __str__(self):
        return str(self.amount)

    class Meta:
        verbose_name = "cash flow record"
        verbose_name_plural = "cash flow records"
