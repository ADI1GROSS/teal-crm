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
    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500"
            })
        self.fields["password1"].widget.attrs["placeholder"] = "סיסמה"
        self.fields["password2"].widget.attrs["placeholder"] = "אימות סיסמה"
        self.fields["username"].widget.attrs["placeholder"] = "שם משתמש"
        self.fields["username"].help_text = "שם המשתמש ישמש להתחברות למערכת"
        self.fields["password1"].help_text = "לפחות 8 תווים, לא סיסמה נפוצה, ולא מספרים בלבד"
        self.fields["password2"].help_text = "יש להזין את אותה סיסמה שוב לאימות"
