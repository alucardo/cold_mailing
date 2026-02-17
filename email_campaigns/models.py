from django.db import models
from django.utils.translation import gettext_lazy as _
from settings.models import EmailAccount, EmailFooter
from mailing_lists.models import MailingList


class Campaign(models.Model):
    """
    Kampania email.
    Łączy listę mailingową, konto email i stopkę.
    """

    class Status(models.TextChoices):
        DRAFT = 'draft', _('Szkic')
        SCHEDULED = 'scheduled', _('Zaplanowana')
        ACTIVE = 'active', _('Aktywna')
        PAUSED = 'paused', _('Wstrzymana')
        COMPLETED = 'completed', _('Zakończona')

    name = models.CharField(
        _("Nazwa kampanii"),
        max_length=200,
        help_text=_("Wewnętrzna nazwa kampanii")
    )

    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        help_text=_("Aktualny status kampanii")
    )

    mailing_list = models.ForeignKey(
        MailingList,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='campaigns',
        verbose_name=_("Lista mailingowa"),
        help_text=_("Lista kontaktów do których zostanie wysłana kampania")
    )

    email_account = models.ForeignKey(
        EmailAccount,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='campaigns',
        verbose_name=_("Konto email"),
        help_text=_("Konto email z którego zostanie wysłana kampania")
    )

    footer = models.ForeignKey(
        EmailFooter,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='campaigns',
        verbose_name=_("Stopka"),
        help_text=_("Stopka dodawana do każdej wiadomości")
    )

    # Metadata
    created_at = models.DateTimeField(_("Data utworzenia"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Data aktualizacji"), auto_now=True)

    class Meta:
        verbose_name = _("Kampania")
        verbose_name_plural = _("Kampanie")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"

    @property
    def is_ready(self):
        """Sprawdza czy kampania ma wszystkie wymagane elementy"""
        return all([
            self.mailing_list,
            self.email_account,
            self.footer,
        ])

    @property
    def wizard_step(self):
        """
        Zwraca aktualny krok wizarda na podstawie uzupełnionych danych.
        Przydatne do przekierowania przy powrocie do niedokończonej kampanii.
        """
        if not self.mailing_list:
            return 2
        if not self.email_account or not self.footer:
            return 3
        return 4