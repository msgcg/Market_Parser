"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))
class CategoryParsingForm(forms.Form):
    category_url = forms.URLField(label='Ссылка на категорию', widget=forms.URLInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите ссылку на категорию Ozon'
    }))

class CategoryParsingYandexForm(forms.Form):
    category_url = forms.URLField(
        label="Ссылка на категорию",
        widget=forms.URLInput(attrs={
            "class": "form-control",
            "placeholder": "Введите ссылку на категорию Яндекс Маркет"
        })
    )
    
class CategoryParsingLamodaForm(forms.Form):
    category_url = forms.URLField(
        label="Ссылка на категорию",
        widget=forms.URLInput(attrs={
            "class": "form-control",
            "placeholder": "Введите ссылку на категорию Lamoda"
        })
    )
    
class CategoryParsingWbForm(forms.Form):
    category_url = forms.URLField(
        label="Ссылка на категорию",
        widget=forms.URLInput(attrs={
            "class": "form-control",
            "placeholder": "Введите ссылку на категорию Wilberries"
        })
    )
