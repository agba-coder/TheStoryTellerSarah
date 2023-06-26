from django import forms
from django.forms import ModelForm
from .models import Comment 


class CommentForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Name"}))
    email = forms.EmailField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Email"}))
    body = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control", "placeholder": "Your Comment"}))
    
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body',]