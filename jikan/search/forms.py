from .models import Paper, Comment, Author
from django.forms import ModelForm, ModelChoiceField
from django import forms
from dal.autocomplete import ModelSelect2

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text',)


class PaperForm(ModelForm):
    journal = ModelChoiceField(
        queryset = Paper.objects.all(),
        widget = ModelSelect2(url='journal_autocomplete')
    )

    authors = ModelChoiceField(
        queryset = Author.objects.all(),
        widget = ModelSelect2(url='author_autocomplete')
    )

    class Meta:
        model = Paper
        fields = ('title', 'authors', 'abstract', 'journal')
