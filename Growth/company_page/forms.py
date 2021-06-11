from django import forms
from django.utils.safestring import mark_safe

from django.utils.translation import ugettext_lazy as _

from .models import Company


class AddCompanyForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super(AddCompanyForm, self).__init__(*args, **kwargs)

        self.fields['industry'].label = "Industry*"
        self.fields['size'].label = "Size*"
        self.fields['type'].label = "Type*"
        self.fields['website_url'].help_text = \
            mark_safe('<br><i>URL should start with http:// or https:// or www.</i>')
        self.fields['verify'].required = True
        self.fields['verify'].label = ""


    name = forms.CharField(label=mark_safe('<h5>Company Name*</h5>'), label_suffix='')
    description = forms.CharField(
        label='Description*',
        label_suffix=mark_safe('<br><br'),
        widget=forms.Textarea(
            attrs={
                "placeholder": "A brief introduction of your company's nature of business",
                "rows":5,
                "cols":60
            }
        )
    )

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
            'verify'
        ]



class ModifyCompanyForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super(ModifyCompanyForm, self).__init__(*args, **kwargs)

        self.fields['industry'].label = "Industry*"
        self.fields['size'].label = "Size*"
        self.fields['type'].label = "Type*"

    name = forms.CharField(label=mark_safe('<h5>Company Name*</h5>'), label_suffix='')
    description = forms.CharField(
        label='Description*',
        label_suffix=mark_safe('<br><br'),
        widget=forms.Textarea(
            attrs={
                "placeholder": "A brief introduction of your company's nature of business",
                "rows":5,
                "cols":60
            }
        )
    )

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