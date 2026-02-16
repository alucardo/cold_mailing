from django import forms
from .models import ApiSetting, EmailAccount, EmailFooter
from config.form_styles import (
    FORM_INPUT_CLASS,
    FORM_CHECKBOX_CLASS,
    FORM_TEXTAREA_CLASS,
    FORM_TEXTAREA_MONO_CLASS,
    FORM_SELECT_CLASS,
)

class CreateApiForm(forms.ModelForm):
    class Meta:
        model = ApiSetting
        fields = ['api_type', 'name', 'text']

        # Dodaj klasy CSS do każdego pola
        widgets = {
            'api_type': forms.Select(attrs={
                'class': FORM_SELECT_CLASS
            }),
            'name': forms.TextInput(attrs={
                'class': FORM_INPUT_CLASS
            }),
            'text': forms.Textarea(attrs={
                'rows': 5,
                'class': FORM_TEXTAREA_CLASS
            })
        }


class EmailAccountForm(forms.ModelForm):
    class Meta:
        model = EmailAccount
        fields = [
            'email', 'name', 'from_name',
            'smtp_host', 'smtp_port', 'smtp_username', 'smtp_password', 'smtp_use_tls',
            'imap_host', 'imap_port', 'imap_username', 'imap_password', 'imap_use_ssl',
            'is_active'
        ]

        widgets = {
            'email': forms.EmailInput(attrs={'class': FORM_INPUT_CLASS, 'placeholder': 'kontakt@domena.pl'}),
            'name': forms.TextInput(attrs={'class': FORM_INPUT_CLASS, 'placeholder': 'Sprzedaż 1'}),
            'from_name': forms.TextInput(attrs={'class': FORM_INPUT_CLASS, 'placeholder': 'Jan Kowalski'}),

            'smtp_host': forms.TextInput(attrs={'class': FORM_INPUT_CLASS, 'placeholder': 'smtp.domena.pl'}),
            'smtp_port': forms.NumberInput(attrs={'class': FORM_INPUT_CLASS, 'placeholder': '587'}),
            'smtp_username': forms.TextInput(attrs={'class': FORM_INPUT_CLASS, 'placeholder': 'kontakt@domena.pl'}),
            'smtp_password': forms.PasswordInput(attrs={'class': FORM_INPUT_CLASS, 'placeholder': '••••••••'}),
            'smtp_use_tls': forms.CheckboxInput(attrs={'class': FORM_CHECKBOX_CLASS}),

            'imap_host': forms.TextInput(attrs={'class': FORM_INPUT_CLASS, 'placeholder': 'imap.domena.pl'}),
            'imap_port': forms.NumberInput(attrs={'class': FORM_INPUT_CLASS, 'placeholder': '993'}),
            'imap_username': forms.TextInput(attrs={'class': FORM_INPUT_CLASS, 'placeholder': 'kontakt@domena.pl'}),
            'imap_password': forms.PasswordInput(attrs={'class': FORM_INPUT_CLASS, 'placeholder': '••••••••'}),
            'imap_use_ssl': forms.CheckboxInput(attrs={'class': FORM_CHECKBOX_CLASS}),

            'is_active': forms.CheckboxInput(attrs={'class': FORM_CHECKBOX_CLASS}),
        }

    def __init__(self, *args, **kwargs):
        """
        Przy edycji hasła są opcjonalne.
        Jeśli puste - nie zmieniamy, jeśli wypełnione - zapisujemy nowe.
        """
        super().__init__(*args, **kwargs)

        # Jeśli to edycja (instance istnieje) - hasła opcjonalne
        if self.instance and self.instance.pk:
            self.fields['smtp_password'].required = False
            self.fields['imap_password'].required = False

            # Zmień placeholder dla jasności
            self.fields['smtp_password'].widget.attrs['placeholder'] = 'Pozostaw puste aby nie zmieniać'
            self.fields['imap_password'].widget.attrs['placeholder'] = 'Pozostaw puste aby nie zmieniać'

    def clean_smtp_password(self):
        """Jeśli puste przy edycji - zachowaj stare hasło"""
        password = self.cleaned_data.get('smtp_password')

        # Jeśli edycja i hasło puste - zwróć stare
        if self.instance and self.instance.pk and not password:
            return self.instance.smtp_password

        return password

    def clean_imap_password(self):
        """Jeśli puste przy edycji - zachowaj stare hasło"""
        password = self.cleaned_data.get('imap_password')

        # Jeśli edycja i hasło puste - zwróć stare
        if self.instance and self.instance.pk and not password:
            return self.instance.imap_password

        return password

class TestEmailForm(forms.Form):
    """Formularz do testowania wysyłania emaili"""
    recipient_email = forms.EmailField(
        label="Adres odbiorcy",
        help_text="Email na który zostanie wysłana wiadomość testowa",
        widget=forms.EmailInput(attrs={
            'class': FORM_INPUT_CLASS,
            'placeholder': 'test@example.com'
        })
    )


class EmailFooterForm(forms.ModelForm):
    """Formularz do tworzenia/edycji stopek email"""

    class Meta:
        model = EmailFooter
        fields = ['name', 'html_content', 'is_default']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': FORM_INPUT_CLASS,
                'placeholder': 'Stopka promocyjna'
            }),
            'html_content': forms.Textarea(attrs={
                'class': FORM_TEXTAREA_MONO_CLASS,
                'rows': 15,
                'placeholder': '''<div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #e0e0e0;">
                      <p style="color: #666; font-size: 14px;">
                        Pozdrawiam,<br>
                        <strong>Jan Kowalski</strong><br>
                        Specjalista ds. Sprzedaży<br>
                        email@firma.pl | +48 123 456 789
                      </p>
                    </div>'''
            }),
            'is_default': forms.CheckboxInput(attrs={
                'class': FORM_CHECKBOX_CLASS
            }),
        }

        labels = {
            'name': 'Nazwa stopki',
            'html_content': 'Kod HTML stopki',
            'is_default': 'Ustaw jako domyślną',
        }

        help_texts = {
            'name': 'Nazwa opisowa stopki (np. "Stopka promocyjna", "Stopka standard")',
            'html_content': 'Pełny kod HTML stopki. Użyj inline CSS dla stylowania.',
            'is_default': 'Jeśli zaznaczone, ta stopka będzie używana domyślnie dla tego konta',
        }