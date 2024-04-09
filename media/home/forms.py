from django import forms
from .models import Post ,Comment

class PostUpdateForms(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control'})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body':forms.Textarea(attrs={'class':'form-control','rows':'6'})
        }

class ReplyCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body':forms.Textarea(attrs={'class':'form-control','rows':'4'})
        }

class PostSearchForm(forms.Form):

    search = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'search...'}))