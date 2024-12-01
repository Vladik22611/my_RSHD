from django import forms
from django.contrib.auth.models import User


class NameForm(forms.Form):
    your_name = forms.CharField(label="Your name", max_length=100)


class DateForm(forms.Form):
    date = forms.DateField(input_formats=["%d/%m/%Y"])


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                "class": "single-input",
                "title": "password1",
                "placeholder": "Пароль",
                "onfocus": "this.placeholder = ''",
                "onblur": "this.placeholder = 'Пароль'",
            }
        ),
    )
    password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                "class": "single-input",
                "title": "password2",
                "placeholder": "Повторите пароль",
            }
        ),
    )
    username = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={"class": "single-input", "title": "username", "placeholder": "Логин"}
        ),
    )
    email = forms.EmailField(
        label="",
        widget=forms.EmailInput(
            attrs={"class": "single-input", "title": "email", "placeholder": "E-mail"}
        ),
    )

    class Meta:
        model = User
        fields = ("username", "email")

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Пароли не совпадают...")
        return cd["password2"]


class LoginForm(forms.Form):
    username = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "single-input",
                "title": "username",
                "placeholder": "Логин",
                "autofocus": True,
            }
        ),
    )
    password = forms.CharField(
        label="",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "single-input",
                "title": "password1",
                "placeholder": "Пароль",
                "onfocus": "this.placeholder = ''",
                "onblur": "this.placeholder = 'Пароль'",
            }
        ),
    )
