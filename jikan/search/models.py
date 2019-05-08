from django.db.models import CharField, Model, IntegerField, ForeignKey, ManyToManyField, PROTECT
from django.db import models


class Paper(models.Model):
#   store the academic paper information
    aminer_id = CharField(max_length=100, null=True)
    title = CharField(max_length=1000)
    journal = ForeignKey('Journal', related_name='papers', null=True, on_delete=PROTECT)
    year = IntegerField(null=True)
    abstract = CharField(max_length=10000, null=True)
    authors = ManyToManyField('Author', related_name='papers', null=True)
    reference = ForeignKey('self', on_delete=models.CASCADE, null=True)

class Journal(models.Model):
    name = CharField(max_length=500)

class Author(models.Model):
    last_name = CharField(max_length=100)
    first_name = CharField(max_length=100)