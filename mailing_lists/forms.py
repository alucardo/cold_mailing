from django import forms
from .models import MailingList, Contact


class MailingListForm(forms.ModelForm):
    class Meta:
        model = MailingList
        fields = ['name']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'relative block w-full appearance-none rounded-lg px-[calc(--spacing(3.5)-1px)] py-[calc(--spacing(2.5)-1px)] text-base/6 text-zinc-950 border border-zinc-950/10 bg-transparent dark:bg-white/5 dark:text-white',
                'placeholder': 'np. Klienci Q1 2026'
            })
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['email', 'name']  # ← DODAJ email!

        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'relative block w-full appearance-none rounded-lg px-[calc(--spacing(3.5)-1px)] py-[calc(--spacing(2.5)-1px)] text-base/6 text-zinc-950 border border-zinc-950/10 bg-transparent dark:bg-white/5 dark:text-white',
                'placeholder': 'jan@example.com'
            }),
            'name': forms.TextInput(attrs={
                'class': 'relative block w-full appearance-none rounded-lg px-[calc(--spacing(3.5)-1px)] py-[calc(--spacing(2.5)-1px)] text-base/6 text-zinc-950 border border-zinc-950/10 bg-transparent dark:bg-white/5 dark:text-white',
                'placeholder': 'Jan Kowalski (opcjonalne)'
            })
        }

    def __init__(self, *args, mailing_list=None, **kwargs):
        """
        Inicjalizacja formularza z listą mailingową.
        Potrzebne do walidacji duplikatów.
        """
        super().__init__(*args, **kwargs)
        self.mailing_list = mailing_list
        # Name jest opcjonalne
        self.fields['name'].required = False

    def clean_email(self):
        """
        Walidacja - sprawdź czy email już istnieje na tej liście
        """
        email = self.cleaned_data.get('email')

        if self.mailing_list and Contact.objects.filter(
                mailing_list=self.mailing_list,
                email=email
        ).exists():
            raise forms.ValidationError(
                f'Adres {email} już istnieje na tej liście mailingowej.'
            )

        return email