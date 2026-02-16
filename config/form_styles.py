"""
Globalne style CSS dla formularzy w całym projekcie.
Używa Tailwind CSS.

Użycie:
    from config.form_styles import FORM_INPUT_CLASS, FORM_CHECKBOX_CLASS

    class MyForm(forms.ModelForm):
        widgets = {
            'email': forms.EmailInput(attrs={'class': FORM_INPUT_CLASS}),
            'is_active': forms.CheckboxInput(attrs={'class': FORM_CHECKBOX_CLASS}),
        }
"""

# ============================================
# POLA TEKSTOWE
# ============================================

FORM_INPUT_CLASS = (
    'relative block w-full appearance-none rounded-lg '
    'px-[calc(--spacing(3.5)-1px)] py-[calc(--spacing(2.5)-1px)] '
    'text-base/6 text-zinc-950 border border-zinc-950/10 '
    'bg-transparent dark:bg-white/5 dark:text-white'
)


# ============================================
# TEXTAREA
# ============================================

FORM_TEXTAREA_CLASS = (
    'relative block w-full appearance-none rounded-lg '
    'px-[calc(--spacing(3.5)-1px)] py-[calc(--spacing(2.5)-1px)] '
    'text-base/6 text-zinc-950 border border-zinc-950/10 '
    'bg-transparent dark:bg-white/5 dark:text-white'
)

# Textarea z czcionką monospace (dla kodu HTML, JSON, etc.)
FORM_TEXTAREA_MONO_CLASS = (
    'relative block w-full appearance-none rounded-lg '
    'px-[calc(--spacing(3.5)-1px)] py-[calc(--spacing(2.5)-1px)] '
    'text-base/6 text-zinc-950 border border-zinc-950/10 '
    'bg-transparent dark:bg-white/5 dark:text-white '
    'font-mono text-sm'
)


# ============================================
# CHECKBOXY I RADIO
# ============================================

FORM_CHECKBOX_CLASS = 'rounded border-zinc-950/10 dark:border-white/10'
FORM_RADIO_CLASS = 'rounded-full border-zinc-950/10 dark:border-white/10'


# ============================================
# SELECT / DROPDOWN
# ============================================

FORM_SELECT_CLASS = (
    'relative block w-full appearance-none rounded-lg '
    'px-[calc(--spacing(3.5)-1px)] py-[calc(--spacing(2.5)-1px)] '
    'text-base/6 text-zinc-950 border border-zinc-950/10 '
    'bg-transparent dark:bg-white/5 dark:text-white'
)


# ============================================
# PLIK
# ============================================

FORM_FILE_CLASS = (
    'relative block w-full appearance-none rounded-lg '
    'px-[calc(--spacing(3.5)-1px)] py-[calc(--spacing(2.5)-1px)] '
    'text-base/6 text-zinc-950 border border-zinc-950/10 '
    'bg-transparent dark:bg-white/5 dark:text-white'
)