from django import forms
from django.forms import inlineformset_factory
from .models import Lead, Contact

class AddLeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['bride_side', 'groom_side', 'day' ,'hebrew_day','hebrew_month','hebrew_year', 'date_gregorian','hour', 'hall', 'address', 'additional_details', 'video','assistent','additional_crew','status','payment_status','payment_method']
        widgets = {
            'date_gregorian': forms.DateInput(
                attrs={
                    'type': 'date',
                    'placeholder': 'יום-חודש-שנה',
                    'class': 'form-input'
                }
            ),
        }

class AddLeadFormPublic(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['bride_side', 'groom_side', 'address', 'day' ,'hebrew_day','hebrew_month','hebrew_year', 'date_gregorian', 'hall','has_additional_crew','payment_method']
        widgets = {
            'date_gregorian': forms.DateInput(
                attrs={
                    'type': 'date',
                    'placeholder': 'יום-חודש-שנה',
                    'class': 'form-input'
                }
            ),
        }

class AddContactForm(forms.ModelForm):
    def __init__(self, *args, role=None, hide_role=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.role = role

        if hide_role:
            self.fields['role'].widget = forms.HiddenInput()

    class Meta:
        model = Contact
        fields = ['first_name','second_name', 'phone','email','concat_address','role']

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.role:
            instance.role = self.role
        if commit:
            instance.save()
        return instance


ContactFormSet = inlineformset_factory(
    Lead, Contact,
    form=AddContactForm,
    extra=4,
    can_delete= True
)
ContactFormSetPublic = inlineformset_factory(
    Lead, Contact,
    form=AddContactForm,
    can_delete=False  # dont allow delete
)