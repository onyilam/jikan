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
    ("3", "Ready for Submission"),
    ("4", "Submitted"), ("5", "Revising"), ("6", "In Print")]
    status = forms.ChoiceField(choices=c, label="Status")
    document = forms.FileField(required=False, label="File")

    class Meta:
        model = Paper
        fields = ('title', 'abstract', 'status', 'document',)


class EditPaperForm(PaperForm):
    class Meta:
        model = Paper
        # widgets = ModelChoiceField(
        #     'myformfield': ModelSelect2(
        #         # ...
        #     ),
        # )
        fields = ('title', 'abstract', 'status', 'document', 'authors')
