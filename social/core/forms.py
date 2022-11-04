# dwitter/forms.py

from django import forms
from .models import Dweet

class DweetForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Dweet something...",
                "class": "textarea is-success is-medium",
            }
        ),
        label="",
    ),
    # like = forms.IntegerField(
    #     widget=forms.widgets.TextInput(
    #         required=True,
    #     ),
    # ),
    class Meta:
        model = Dweet
        exclude = ("user", )