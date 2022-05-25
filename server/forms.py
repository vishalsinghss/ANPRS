from django import forms

class ResolveNumberPlateForm(forms.Form):
    image = forms.ImageField()