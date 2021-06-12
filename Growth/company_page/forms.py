from django import forms

from .models import Company

class AddCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            'name',
            'description',
            'industry',
            'size',
            'type',
            'location',
            'website_url',
            'logo',
        ]

class ModifyCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            'name',
            'description',
            'industry',
            'size',
            'type',
            'location',
            'website_url',
            'logo'
        ]