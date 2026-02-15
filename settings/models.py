from django.db import models
from django.utils.translation import gettext_lazy as _
from encrypted_model_fields.fields import EncryptedTextField

# Create your models here.
class ApiType(models.Model):
    name = models.CharField(max_length=200, unique=True)
    def __str__(self):
        return self.name

class ApiSetting(models.Model):
    api_type = models.ForeignKey(
        ApiType,
        on_delete=models.CASCADE,
        verbose_name=_("API Type"),
        help_text=_("Wybierz typ API (np. OpenAI, Anthropic)")  # ← DODAJ
    )
    name = models.CharField(
        max_length=200,
        verbose_name=_("Name"),
        help_text=_("Twoja wewnętrzna nazwa klucza API")  # ← LEPSZY TEKST
    )
    text = models.TextField(
        verbose_name=_("Value"),
        help_text=_("Klucz API lub inny tekst konfiguracyjny")  # ← LEPSZY TEKST
    )
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    def __str__(self):
        return self.name


class EmailAccount(models.Model):
    """Konto email do wysyłania i odbierania wiadomości"""

    # Podstawowe informacje
    email = models.EmailField(
        _("Email"),
        unique=True,
        help_text=_("Adres email konta")
    )
    name = models.CharField(
        _("Name/Alias"),
        max_length=200,
        help_text=_("Wewnętrzna nazwa konta (np. 'Sprzedaż 1')")
    )
    from_name = models.CharField(
        _("From Name"),
        max_length=200,
        help_text=_("Imię/nazwa nadawcy wyświetlana w emailu (np. 'Jan z Firmy')")
    )

    # SMTP - wysyłanie emaili
    smtp_host = models.CharField(
        _("SMTP Host"),
        max_length=255,
        help_text=_("Serwer SMTP (np. 'smtp.domena.pl')")
    )
    smtp_port = models.IntegerField(
        _("SMTP Port"),
        default=587,
        help_text=_("Port SMTP (zazwyczaj 587 dla TLS lub 465 dla SSL)")
    )
    smtp_username = models.CharField(
        _("SMTP Username"),
        max_length=255,
        help_text=_("Nazwa użytkownika SMTP (często ten sam email)")
    )
    smtp_password = EncryptedTextField(
        _("SMTP Password"),
        help_text=_("Hasło SMTP (zaszyfrowane)")
    )
    smtp_use_tls = models.BooleanField(
        _("SMTP Use TLS"),
        default=True,
        help_text=_("Użyj TLS dla SMTP")
    )

    # IMAP - odbieranie emaili
    imap_host = models.CharField(
        _("IMAP Host"),
        max_length=255,
        help_text=_("Serwer IMAP (np. 'imap.domena.pl')")
    )
    imap_port = models.IntegerField(
        _("IMAP Port"),
        default=993,
        help_text=_("Port IMAP (zazwyczaj 993 dla SSL)")
    )
    imap_username = models.CharField(
        _("IMAP Username"),
        max_length=255,
        help_text=_("Nazwa użytkownika IMAP (często ten sam email)")
    )
    imap_password = EncryptedTextField(
        _("IMAP Password"),
        help_text=_("Hasło IMAP (zaszyfrowane)")
    )
    imap_use_ssl = models.BooleanField(
        _("IMAP Use SSL"),
        default=True,
        help_text=_("Użyj SSL dla IMAP")
    )

    # Status
    is_active = models.BooleanField(
        _("Is Active"),
        default=True,
        help_text=_("Czy konto jest aktywne")
    )

    # Metadata
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _("Email Account")
        verbose_name_plural = _("Email Accounts")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.email})"