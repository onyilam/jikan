from .models import Paper, Comment
from django.forms import ModelForm
from django import forms

class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)

class PaperForm(ModelForm):

    class Meta:
        model = Paper
        fields = ('title', 'authors', 'abstract', 'year', 'journal')
