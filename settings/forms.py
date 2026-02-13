from django import forms
from .models import ApiSetting, ApiType


class CreateApiForm(forms.ModelForm):
    class Meta:
        model = ApiSetting
        fields = ['api_type', 'name', 'text']

        # Dodaj klasy CSS do każdego pola
        widgets = {
            'api_type': forms.Select(attrs={
                'class': 'relative block w-full appearance-none rounded-lg px-[calc(--spacing(3.5)-1px)] py-[calc(--spacing(2.5)-1px)] text-base/6 text-zinc-950 border border-zinc-950/10 bg-transparent dark:bg-white/5 dark:text-white'
            }),
            'name': forms.TextInput(attrs={
                'class': 'relative block w-full appearance-none rounded-lg px-[calc(--spacing(3.5)-1px)] py-[calc(--spacing(2.5)-1px)] text-base/6 text-zinc-950 border border-zinc-950/10 bg-transparent dark:bg-white/5 dark:text-white'
            }),
            'text': forms.Textarea(attrs={
                'rows': 5,
                'class': 'relative block w-full appearance-none rounded-lg px-[calc(--spacing(3.5)-1px)] py-[calc(--spacing(2.5)-1px)] text-base/6 text-zinc-950 border border-zinc-950/10 bg-transparent dark:bg-white/5 dark:text-white'
            })
        }
