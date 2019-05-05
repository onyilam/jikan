from django.db import models

class Paper(models.Model):
#   store the academic paper information
    title = models.CharField(max_length=1000)
    venue = models.CharField(max_length=200)
    year = models.IntegerField()
    abstract = models.CharField(max_length = 10000)
    authors = models.CharField(max_length = 1000)
    reference = models.ForeignKey('self', on_delete=models.CASCADE)


