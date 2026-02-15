import imaplib
import ssl
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import EmailMessage, get_connection
from ..models import EmailAccount
from ..forms import EmailAccountForm, TestEmailForm
from ..services import test_smtp_connection, test_imap_connection


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


def show_email_account_view(request, pk):
    """Szczegóły konta e-mail + test wysyłania SMTP + test IMAP"""
    account = get_object_or_404(EmailAccount, pk=pk)

    if request.method == 'POST':
        test_type = request.POST.get('test_type')

        if test_type == 'smtp':
            form = TestEmailForm(request.POST)
            if form.is_valid():
                recipient = form.cleaned_data['recipient_email']

                # Użyj serwisu
                success, msg = test_smtp_connection(account, recipient)

                if success:
                    messages.success(request, f'✅ SMTP: {msg}')
                else:
                    messages.error(request, f'❌ SMTP: {msg}')

        elif test_type == 'imap':
            # Użyj serwisu
            success, msg = test_imap_connection(account)

            if success:
                messages.success(request, f'✅ IMAP: {msg}')
            else:
                messages.error(request, f'❌ IMAP: {msg}')

        return redirect('settings:show_email_account', pk=pk)
    else:
        form = TestEmailForm(initial={'recipient_email': account.email})

    return render(request, 'settings/show_email_account.html', {
        'account': account,
        'test_form': form
    })

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