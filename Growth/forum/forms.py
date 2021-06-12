from .models import Comment
from django import forms


class CommentForm(forms.ModelForm):
    text = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={'rows': '1',
                   'placeholder': 'Comment here....'}
        ))

    class Meta:
        model = Comment
        fields = ['text']