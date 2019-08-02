from .models import Paper, ViewerComment, Author, PaperEvent, Attachment
from django.forms import ModelForm, ModelChoiceField, MultipleChoiceField
from django import forms
from dal.autocomplete import ModelSelect2
from multiupload.fields import MultiFileField


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
        fields = ('title', 'abstract', 'status', 'document', 'authors')


class EventForm(ModelForm):
    class Meta:
        model = PaperEvent
        fields = '__all__'
        exclude = ('paper', 'likes', 'frowns')
        widgets = {
          'comment': forms.Textarea(attrs={'rows':4, 'cols':15}),
        }
        help_texts = {
            'date': 'MM/DD/YYYY',
        }
    
    files = MultiFileField(min_num=1, max_num=5)

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['comment'].required = False
        self.fields['files'].required = False

    def save(self, commit=True):
        instance = super(EventForm, self).save(commit)
        for each in self.cleaned_data['files']:
            Attachment.objects.create(file=each, event=instance)
        return instance
