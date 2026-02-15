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
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={})
        }