from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from easy_select2 import Select2

from recipes.models import RecipeCategory
from .models import Profile


def validate_password_strength(value):
    """Validates that a password is as least 7 characters long and has at least
    1 digit and 1 letter.
    """
    min_length = 7

    if len(value) < min_length:
        raise ValidationError(_('Password must be at least {0} characters '
                                'long.').format(min_length))

    # check for digit
    if not any(char.isdigit() for char in value):
        raise ValidationError(_('Password must contain at least 1 digit.'))

    # check for letter
    if not any(char.isalpha() for char in value):
        raise ValidationError(_('Password must contain at least 1 letter.'))


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')
    #
    # def __init__(self, *args, **kwargs):
    #     super(UserRegistrationForm, self).__init__(*args, **kwargs)
    #     if self.fields['password'].validators.append(validate_password_strength):
    #         raise forms.ValidationError('Passwords don\'t match.')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        if validate_password_strength(cd['password']):
            raise forms.ValidationError('Passwords are too short.')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')
