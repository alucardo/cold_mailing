"""
Serwis do testowania połączeń SMTP.
"""

from django.core.mail import EmailMessage, get_connection
from ..models import EmailAccount


def test_smtp_connection(account: EmailAccount, recipient_email: str) -> tuple[bool, str]:
    """
    Testuje połączenie SMTP wysyłając email testowy.

    Args:
        account: Konto email do przetestowania
        recipient_email: Adres odbiorcy wiadomości testowej

    Returns:
        tuple: (success: bool, message: str)
        - success: True jeśli wysłano pomyślnie, False w przypadku błędu
        - message: Komunikat sukcesu lub opis błędu

    Example:
        >>> success, msg = test_smtp_connection(account, 'test@example.com')
        >>> if success:
        >>>     print(f"Sukces: {msg}")
    """
    try:
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

        email = EmailMessage(
            subject=f'Test połączenia - {account.name}',
            body=f'''To jest testowa wiadomość z konta: {account.name}

            Email: {account.email}
            Wysłano: {account.created_at.strftime("%d.%m.%Y %H:%M")}
            
            Jeśli widzisz tę wiadomość, połączenie SMTP działa poprawnie!
            
            ---
            Cold Mailing System''',
            from_email=f'{account.from_name} <{account.email}>',
            to=[recipient_email],
            connection=connection,
        )

        email.send()

        return True, f'Email testowy wysłany pomyślnie na adres {recipient_email}'

    except Exception as e:
        return False, f'Błąd podczas wysyłania: {str(e)}'