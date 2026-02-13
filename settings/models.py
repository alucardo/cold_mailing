from django.db import models
from django.utils.translation import gettext_lazy as _

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

