from typing import Required
from django import forms
from django.forms import fields

from maricon import models
from maricon.models import PaperAbstract, TravelGrant


class PaperAbstractForm(forms.ModelForm):
    class Meta:
        model = PaperAbstract
        fields = ['title', 'authors', 'abstract', 'keywords', 'file', 'theme','presentation']

class TravelGrantForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = TravelGrant
        fields = ['email', 'bank_name', 'acc_number', 'ifsc', 'cv']
        labels = {
            'email': 'E-Mail',
            'bank_name': 'Bank Name',
            'acc_number': 'Account Number',
            'ifsc': 'IFSC Code',
            'cv': 'Resume',
        }
        
    def clean_email(self):
        return self.cleaned_data.get('email')
