from django import forms


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)









# from django.contrib.auth.forms import UserCreationForm
#
#
# class CustomUserCreationForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         fields = UserCreationForm.Meta.fields + ("email",)