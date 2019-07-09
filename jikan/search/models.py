from django.db.models import CharField, Model, IntegerField, TextField, DateField, DateTimeField, FileField, BooleanField, ForeignKey, ManyToManyField, PROTECT, CASCADE
from django.db import models
from users.models import CustomUser
from django.core.validators import MaxValueValidator
from django.conf import settings
from datetime import date

STATUS_OPTIONS =[("1", "Early Development"), ("2", "Writing and Editing"),
("3", "Ready for Submission"),
("4", "Submitted"), ("5", "Revising"), ("6", "In Print")]

VENUE_OPTIONS = [("1", "Conference"), ("2", "Journal")]

EVENT_OPTIONS = [  ("1", "Working Paper"), ( "2", "Presentation"), ("3", "Submitted"),
("4", "Rejected"), ("5", "Revise and Resubmitted"), ("6", "Accepted"), ("7", "Appeared in Journal")]

class Paper(models.Model):
#   store the academic paper information
    aminer_id = CharField(max_length=100, null=True)
    title = CharField(max_length=1000)
    journal = ForeignKey('Journal', related_name='papers', null=True, on_delete=PROTECT)
    year = IntegerField(null=True)
    abstract = TextField(max_length=10000, null=True)
    authors = ManyToManyField('Author', related_name='papers', null=True)
    n_citation = IntegerField(null=True)
    status = CharField(max_length=100, null=True, choices=STATUS_OPTIONS)
    recommend = ManyToManyField('self', null=True)
    likes = IntegerField(default=0)
    dislikes = IntegerField(default=0)
    document = FileField(upload_to='documents/', null=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, null= True)
    created_by = ForeignKey(settings.AUTH_USER_MODEL,
                            related_name='papers',
                            null=True, on_delete=CASCADE)

    def year_month_created(self):
        return self.created_date.strftime('%Y-%m-%d')

    def year_month_modified(self):
        return self.modified_date.strftime('%Y-%m-%d')


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
    """
    stores referee comments.
    """
    paper = ForeignKey(Paper, on_delete=models.CASCADE, related_name='comments')
    venue = CharField(max_length=50, null=True, choices=VENUE_OPTIONS)
    text = TextField()
    date = DateTimeField(null=True)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text


class PaperEvent(models.Model):
    """
    information about the status stage of paper
    """
    paper = ForeignKey(Paper, on_delete=models.CASCADE, related_name='events')
    date = DateTimeField(null=True, help_text="format (mm/dd/yyyy)")
    event = CharField(max_length=50, null=True, choices=EVENT_OPTIONS)
    comment = TextField()
    document = FileField(upload_to='documents/', null=True)
