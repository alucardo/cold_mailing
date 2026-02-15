from django.db import models
from django.utils.translation import gettext_lazy as _


class MailingList(models.Model):
    name = models.CharField(
        _("Name"),
        max_length=200,
        help_text=_("Nazwa listy mailingowej (np. 'Klienci Q1 2026')")
    )
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _("Mailing List")
        verbose_name_plural = _("Mailing Lists")
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def total_contacts(self):
        """Całkowita liczba kontaktów na liście"""
        return self.contacts.count()

    def active_contacts(self):
        """Liczba aktywnych kontaktów"""
        return self.contacts.filter(status='active').count()

    def contact_summary(self):
        """Podsumowanie: '5 z 10'"""
        active = self.active_contacts()
        total = self.total_contacts()
        return f"{active} z {total}"


class Contact(models.Model):
    """Kontakt w liście mailingowej"""

    class Status(models.TextChoices):
        ACTIVE = 'active', _('Aktywny')
        PAUSED = 'paused', _('Wstrzymany')
        COMPLETED = 'completed', _('Zakończony')

    mailing_list = models.ForeignKey(
        MailingList,
        on_delete=models.CASCADE,
        related_name='contacts',
        verbose_name=_("Mailing List")
    )
    email = models.EmailField(
        _("Email"),
        help_text=_("Adres e-mail kontaktu")
    )
    name = models.CharField(
        _("Name"),
        max_length=200,
        help_text=_("Imię/nazwa kontaktu")
    )
    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE
    )
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")
        ordering = ['mailing_list', 'name']
        unique_together = [['mailing_list', 'email']]  # walidacja by e-mail byłunikalny na liście

    def __str__(self):
        return f"{self.name} ({self.email})"