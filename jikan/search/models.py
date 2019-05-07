from django.db import models

class Paper(models.Model):
#   store the academic paper information
    aminer_id = models.CharField(max_length=100, null=True)
    title = models.CharField(max_length=1000)
    venue = models.CharField(max_length=200, null=True)
    year = models.IntegerField(null=True)
    abstract = models.CharField(max_length = 10000, null=True)
    authors = models.CharField(max_length = 1000, null=True)
    reference = models.ForeignKey('self', on_delete=models.CASCADE, null=True)


