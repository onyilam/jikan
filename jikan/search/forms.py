from .models import Paper, Comment
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

    class Meta:
        model = Paper
        fields = ('title', 'abstract', 'journal')
