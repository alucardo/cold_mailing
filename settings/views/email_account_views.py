from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import EmailMessage, get_connection
from ..models import EmailAccount
from ..forms import EmailAccountForm, TestEmailForm


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
    """Szczegóły konta e-mail + test wysyłania"""
    account = get_object_or_404(EmailAccount, pk=pk)

    if request.method == 'POST':
        form = TestEmailForm(request.POST)
        if form.is_valid():
            recipient = form.cleaned_data['recipient_email']

            try:
                # Konfiguracja połączenia SMTP z danymi z konta
                connection = get_connection(
                    backend='django.core.mail.backends.smtp.EmailBackend',
                    host=account.smtp_host,
                    port=account.smtp_port,
                    username=account.smtp_username,
                    password=account.smtp_password,
                    use_tls=account.smtp_use_tls,
                    fail_silently=False,
                    timeout=10,
                )

                # Treść testowej wiadomości
                email = EmailMessage(
                    subject=f'Test połączenia - {account.name}',
                    body=f'''To jest testowa wiadomość z konta: {account.name}
                        Email: {account.email}
                        Wysłano: {account.created_at.strftime("%d.m.Y %H:%M")}
                        
                        Jeśli widzisz tę wiadomość, połączenie SMTP działa poprawnie!
                        
                        ---
                        Cold Mailing System''',
                    from_email=f'{account.from_name} <{account.email}>',
                    to=[recipient],
                    connection=connection,
                )

                # Wyślij email
                email.send()

                messages.success(
                    request,
                    f'✅ Email testowy wysłany pomyślnie na adres {recipient}'
                )

            except Exception as e:
                messages.error(
                    request,
                    f'❌ Błąd podczas wysyłania: {str(e)}'
                )

            # Przekieruj do tego samego widoku (POST-Redirect-GET pattern)
            return redirect('settings:show_email_account', pk=pk)
    else:
        # GET - pokaż pusty formularz
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