"""
All entities which are stored in DB
"""

from django.db import models


MAXCHARINNAME = 40 # Just a simple constant


class Category(models.Model):
    """Represents the category of records."""
    name = models.CharField(max_length=MAXCHARINNAME, unique=True)


class Subcategory(models.Model):
    """Represents the subcategory of records."""
    name = models.CharField(max_length=MAXCHARINNAME, unique=True)
    base_category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Status(models.Model):
    """Represents the status of records."""
    name = models.CharField(max_length=MAXCHARINNAME, unique=True)


class Type(models.Model):
    """Represents the type of records."""
    name = models.CharField(max_length=MAXCHARINNAME, unique=True)


class CashFlowRecord(models.Model):
    """Represents a cash flow record. Be careful, status, type, subcategory and comment fields can be null."""
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True)
    amount = models.FloatField()
    datestamp = models.fields.DateField()
    comment = models.TextField(null=True)
