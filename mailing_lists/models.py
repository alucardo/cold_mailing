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