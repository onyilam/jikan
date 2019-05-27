from .models import Paper, Comment
from django.forms import ModelForm

class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)