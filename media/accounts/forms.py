from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from . import models
class UserRegisterationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"example@gmail.com","class":"form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':" password","class":"form-control"}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':" password confirm","class":"form-control"}))


    def clean_email(self):
        
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError("this email already exists")
        return email


    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).exists()
        if user:
            raise ValidationError("this username already exists")

        return username

    def clean(self):
        cd = super().clean()
        p1 = cd.get('password')
        p2 = cd.get('password_confirm')
        if p1 and p2 and p1 != p2:
            raise ValidationError("password must be math")

class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': " password", "class": "form-control"}))


class EditUserForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={"class":'form-control'}))

    class Meta:
        model=models.Profile
        fields = ['age','bio']
        widgets = {
            'bio':forms.Textarea(attrs={'class':'form-control','rows':'4'}),
            'age':forms.TextInput(attrs={'class':'form-control','rows':'4'})
        }