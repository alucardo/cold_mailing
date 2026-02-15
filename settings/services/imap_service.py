"""
Serwis do testowania połączeń IMAP.
"""

import imaplib
from ..models import EmailAccount


def test_imap_connection(account: EmailAccount) -> tuple[bool, str]:
    """
    Testuje połączenie IMAP i sprawdza liczbę wiadomości w INBOX.

    Args:
        account: Konto email do przetestowania

    Returns:
        tuple: (success: bool, message: str)
        - success: True jeśli połączono pomyślnie, False w przypadku błędu
        - message: Komunikat z liczbą wiadomości lub opis błędu

    Example:
        >>> success, msg = test_imap_connection(account)
        >>> if success:
        >>>     print(f"IMAP OK: {msg}")
    """
    try:
        # Połącz się z IMAP
        if account.imap_use_ssl:
            mail = imaplib.IMAP4_SSL(
                account.imap_host,
                account.imap_port,
                timeout=10
            )
        else:
            mail = imaplib.IMAP4(
                account.imap_host,
                account.imap_port,
                timeout=10
            )

        # Zaloguj się
        mail.login(account.imap_username, account.imap_password)

        # Wybierz INBOX
        mail.select('INBOX')

        # Policz wiadomości
        status, data = mail.search(None, 'ALL')
        email_ids = data[0].split()
        count = len(email_ids)

        # Rozłącz
        mail.logout()

        return True, f'Połączenie udane! Znaleziono {count} wiadomości w INBOX.'

    except imaplib.IMAP4.error as e:
        return False, f'Błąd autentykacji - {str(e)}'
    except Exception as e:
        return False, f'Błąd połączenia - {str(e)}'