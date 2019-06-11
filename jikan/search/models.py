from django.db.models import CharField, Model, IntegerField, TextField, DateTimeField, BooleanField, ForeignKey, ManyToManyField, PROTECT, CASCADE
from django.db import models
from users.models import CustomUser
from django.core.validators import MaxValueValidator


class Paper(models.Model):
#   store the academic paper information
    aminer_id = CharField(max_length=100, null=True)
    title = CharField(max_length=1000)
    journal = ForeignKey('Journal', related_name='papers', null=True, on_delete=PROTECT)
    year = IntegerField(null=True)
    abstract = TextField(max_length=10000, null=True)
    authors = ManyToManyField('Author', related_name='papers', null=True)
    n_citation = IntegerField(null=True)
    recommend = ManyToManyField('self', null=True)
    likes = IntegerField(default=0)
    dislikes = IntegerField(default=0)


class Journal(models.Model):
    name = CharField(max_length=500)

    def __str__(self):
        return self.name


class Author(models.Model):
    last_name = CharField(max_length=100)
    first_name = CharField(max_length=100)

    def __str__(self):
        return self.last_name


class Preference(models.Model):
    user = ForeignKey(CustomUser, on_delete=CASCADE, null=True)
    paper = ForeignKey(Paper, on_delete=CASCADE, null=True)
    value = IntegerField(null=True, validators=[
            MaxValueValidator(20)
        ])
    date = DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user) + ':' + str(self.paper) + ':' + str(self.value)

    class Meta:
        unique_together = ("user", "paper", "value")


class Comment(models.Model):
    paper = ForeignKey(Paper, on_delete=models.CASCADE, related_name='comments')
    author = CharField(max_length=200)
    text = TextField()
    created_date = DateTimeField(auto_now=True)
    approved_comment = BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text
