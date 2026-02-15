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
    """Formularz do tworzenia i edycji kontaktu"""

    class Meta:
        model = Contact
        fields = ['email', 'name', 'status']

        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'relative block w-full appearance-none rounded-lg px-[calc(--spacing(3.5)-1px)] py-[calc(--spacing(2.5)-1px)] text-base/6 text-zinc-950 border border-zinc-950/10 bg-transparent dark:bg-white/5 dark:text-white',
                'placeholder': 'jan@example.com'
            }),
            'name': forms.TextInput(attrs={
                'class': 'relative block w-full appearance-none rounded-lg px-[calc(--spacing(3.5)-1px)] py-[calc(--spacing(2.5)-1px)] text-base/6 text-zinc-950 border border-zinc-950/10 bg-transparent dark:bg-white/5 dark:text-white',
                'placeholder': 'Jan Kowalski'
            }),
            'status': forms.Select(attrs={
                'class': 'relative block w-full appearance-none rounded-lg px-[calc(--spacing(3.5)-1px)] py-[calc(--spacing(2.5)-1px)] text-base/6 text-zinc-950 border border-zinc-950/10 bg-transparent dark:bg-white/5 dark:text-white'
            })
        }

    def __init__(self, *args, mailing_list=None, hide_status=True, **kwargs):
        """
        Inicjalizacja formularza.

        Args:
            mailing_list: Lista mailingowa do walidacji
            hide_status: Ukryj pole status (dla tworzenia nowych kontaktów)
        """
        super().__init__(*args, **kwargs)
        self.mailing_list = mailing_list

        # Name jest opcjonalne
        self.fields['name'].required = False

        # Ukryj status przy tworzeniu (zawsze będzie 'active')
        if hide_status:
            self.fields['status'].widget = forms.HiddenInput()
            self.fields['status'].initial = 'active'

    def clean_email(self):
        """Walidacja - sprawdź duplikaty emaili"""
        email = self.cleaned_data.get('email')

        if self.mailing_list:
            # Zapytanie bazowe
            existing = Contact.objects.filter(
                mailing_list=self.mailing_list,
                email=email
            )

            # Jeśli edycja - wykluczamy edytowany kontakt
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)

            if existing.exists():
                raise forms.ValidationError(
                    f'Adres {email} już istnieje na tej liście.'
                )

        return email