from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..models import EmailAccount
from ..forms import EmailAccountForm


def email_accounts_view(request):
    """Lista kont email"""
    accounts = EmailAccount.objects.all()
    return render(request, 'settings/email_accounts.html', {'accounts': accounts})


def create_email_account_view(request):
    """Dodawanie konta email"""
    if request.method == 'POST':
        form = EmailAccountForm(request.POST)
        if form.is_valid():
            account = form.save()
            messages.success(request, f'Dodano konto {account.email}')
            return redirect('settings:email_accounts')
    else:
        form = EmailAccountForm()

    return render(request, 'settings/create_email_account.html', {'form': form})


def edit_email_account_view(request, pk):
    """Edycja konta email"""
    account = get_object_or_404(EmailAccount, pk=pk)

    if request.method == 'POST':
        form = EmailAccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.success(request, f'Zaktualizowano konto {account.email}')
            return redirect('settings:email_accounts')
    else:
        form = EmailAccountForm(instance=account)

    return render(request, 'settings/edit_email_account.html', {
        'form': form,
        'account': account
    })


def delete_email_account_view(request, pk):
    """Usuwanie konta email"""
    account = get_object_or_404(EmailAccount, pk=pk)

    if request.method == 'POST':
        email = account.email
        account.delete()
        messages.success(request, f'Usunięto konto {email}')

    return redirect('settings:email_accounts')