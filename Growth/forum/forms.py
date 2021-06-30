from .models import Comment, Reply
from django import forms


class CommentForm(forms.ModelForm):
    text = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={'rows': '1',
                   'placeholder': 'Comment here....'}
        ))

    class Meta:
        model = Comment
        fields = ['text']

class ReplyForm(forms.ModelForm):
    text = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={'rows': '1',
                   'placeholder': 'Reply here....'}
        ))

    class Meta:
        model = Reply
        fields = ['text']
        