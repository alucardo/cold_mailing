"""
Widoki do zarządzania stopkami email.
Zagnieżdżone pod kontem email.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..models import EmailAccount, EmailFooter
from ..forms import EmailFooterForm


def list_footers_view(request, account_pk):
    """Lista stopek dla danego konta email"""
    account = get_object_or_404(EmailAccount, pk=account_pk)
    footers = account.footers.all()  # używamy related_name='footers'

    return render(request, 'settings/footers/list.html', {
        'account': account,
        'footers': footers
    })


def create_footer_view(request, account_pk):
    """Dodawanie nowej stopki do konta"""
    account = get_object_or_404(EmailAccount, pk=account_pk)

    if request.method == 'POST':
        form = EmailFooterForm(request.POST)
        if form.is_valid():
            footer = form.save(commit=False)
            footer.account = account  # przypisz do konta
            footer.save()

            messages.success(request, f'Dodano stopkę "{footer.name}"')
            return redirect('settings:list_footers', account_pk=account.pk)
    else:
        form = EmailFooterForm()

    return render(request, 'settings/footers/create.html', {
        'account': account,
        'form': form
    })


def edit_footer_view(request, account_pk, pk):
    """Edycja stopki"""
    account = get_object_or_404(EmailAccount, pk=account_pk)
    footer = get_object_or_404(EmailFooter, pk=pk, account=account)

    if request.method == 'POST':
        form = EmailFooterForm(request.POST, instance=footer)
        if form.is_valid():
            form.save()
            messages.success(request, f'Zaktualizowano stopkę "{footer.name}"')
            return redirect('settings:list_footers', account_pk=account.pk)
    else:
        form = EmailFooterForm(instance=footer)

    return render(request, 'settings/footers/edit.html', {
        'account': account,
        'footer': footer,
        'form': form
    })


def delete_footer_view(request, account_pk, pk):
    """Usuwanie stopki"""
    account = get_object_or_404(EmailAccount, pk=account_pk)
    footer = get_object_or_404(EmailFooter, pk=pk, account=account)

    if request.method == 'POST':
        name = footer.name
        footer.delete()
        messages.success(request, f'Usunięto stopkę "{name}"')

    return redirect('settings:list_footers', account_pk=account.pk)