from django.contrib import admin
from .models import Paper, Comment, Author, Journal

admin.site.register(Paper)
admin.site.register(Author)
admin.site.register(Journal)
admin.site.register(Comment)


# Register your models here.
