from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Userprofile

class UserprofileForm(forms.ModelForm):
    class Meta:
        model = Userprofile
        fields = ['name', 'email', 'phone', 'regulations_document']
        labels = {
            'name': 'שם מלא',
            'email': 'אימייל',
            'phone': 'טלפון',
            'regulations_document': 'תקנון'
        }
class CustomSignupForm(UserCreationForm):
    phone = forms.CharField(max_length=20, required=False, label='טלפון')
    #למה אין כאן מייל

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'phone')

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            Userprofile.objects.create(
                user=user,
                email=self.cleaned_data.get('email'),
                phone=self.cleaned_data.get('phone'),
            )
        return user