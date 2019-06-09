from .models import Paper, Comment
from django.forms import ModelForm
from django import forms
from dal import autocomplete

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text',)


class PaperForm(ModelForm):
    journal = forms.ModelChoiceField(
        queryset=Paper.objects.all(),
        widget=autocomplete.ModelSelect2(url='journal_autocomplete')
    )

    class Meta:
        model = Paper
        fields = ('title', 'abstract')
