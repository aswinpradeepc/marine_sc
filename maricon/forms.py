from django import forms

from maricon.models import PaperAbstract


class PaperAbstractForm(forms.ModelForm):
    class Meta:
        model = PaperAbstract
        fields = ['title', 'authors', 'abstract', 'keywords', 'file', 'theme','presentation']
