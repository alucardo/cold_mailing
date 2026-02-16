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


class EmailFooter(models.Model):
    """
    Stopka HTML dla emaili wysyłanych z konta.
    Jedno konto może mieć wiele stopek, jedna jest domyślna.
    """

    account = models.ForeignKey(
        EmailAccount,
        on_delete=models.CASCADE,
        related_name='footers',
        verbose_name=_("Konto email")
    )

    name = models.CharField(
        _("Nazwa stopki"),
        max_length=200,
        help_text=_("Np. 'Stopka promocyjna', 'Stopka standard'")
    )

    html_content = models.TextField(
        _("Treść HTML"),
        help_text=_("Kod HTML stopki wyświetlany pod treścią emaila")
    )

    is_default = models.BooleanField(
        _("Domyślna stopka"),
        default=False,
        help_text=_("Czy ta stopka jest domyślna dla tego konta")
    )

    created_at = models.DateTimeField(_("Data utworzenia"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Data aktualizacji"), auto_now=True)

    class Meta:
        verbose_name = _("Stopka email")
        verbose_name_plural = _("Stopki email")
        ordering = ['-is_default', '-created_at']

    def __str__(self):
        default_marker = " [DOMYŚLNA]" if self.is_default else ""
        return f"{self.name} ({self.account.email}){default_marker}"

    def save(self, *args, **kwargs):
        """
        Jeśli ustawiamy tę stopkę jako domyślną,
        usuń flagę 'default' z innych stopek tego konta.
        """
        if self.is_default:
            # Usuń is_default z innych stopek tego konta
            EmailFooter.objects.filter(
                account=self.account,
                is_default=True
            ).exclude(pk=self.pk).update(is_default=False)

        super().save(*args, **kwargs)