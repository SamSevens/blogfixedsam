# blog/forms.py

from django import forms
from .models import Contest

class NameForm(forms.Form):
    first_name = forms.CharField(label='First name', max_length=50)
    last_name = forms.CharField(label='Last name', max_length=50)


class ContestForm(forms.ModelForm):
    class Meta:
        model = Contest
        fields = ['first_name', 'last_name', 'email', 'photo']
