from .models import Paper, Comment, Author
from django.forms import ModelForm, ModelChoiceField, MultipleChoiceField
from django import forms
from dal.autocomplete import ModelSelect2
#from floppyforms.widgets import input

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text',)


class PaperForm(ModelForm):
    # journal = ModelChoiceField(
    #     queryset = Paper.objects.all(),
    #     empty_label = 'Working Paper',
    #     label = 'Venue',
    #     help_text='The venue the paper appears',
    #     widget = ModelSelect2(url='journal_autocomplete')
    # )
    c =[("1", "Early development"), ("2", "Writing and Editing"),
    ("3", "Subitted"), ("4", "R&R"), ("5", "In Print")]
    status = forms.ChoiceField(choices=c, label="Status")

    class Meta:
        model = Paper
        fields = ('title', 'abstract', 'status')
