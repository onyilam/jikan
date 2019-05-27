from .models import Paper, Comment
from django.forms import ModelForm

class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)

class PaperForm(ModelForm):

    class Meta:
        model = Paper
        fields = ('title', 'abstract',)