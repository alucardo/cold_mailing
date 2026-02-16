from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from config.form_styles import FORM_INPUT_CLASS


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

        widgets = {
            'username': forms.TextInput(attrs={
                'class': FORM_INPUT_CLASS,
                'placeholder': 'nazwa_uzytkownika'
            }),
            'email': forms.EmailInput(attrs={
                'class': FORM_INPUT_CLASS,
                'placeholder': 'twoj@email.pl'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].widget.attrs.update({
            'class': FORM_INPUT_CLASS,
            'placeholder': 'Wprowadź hasło'
        })
        self.fields['password2'].widget.attrs.update({
            'class': FORM_INPUT_CLASS,
            'placeholder': 'Powtórz hasło'
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user