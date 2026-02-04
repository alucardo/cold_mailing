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
        verbose_name=_("API Type")
    )
    name = models.CharField(
        max_length=200,
        help_text="Nazwa ustawienia (np. 'API Key', 'Endpoint')"
    )
    text = models.TextField(
        verbose_name="Wartość",
        help_text="Wartość ustawienia"
    )
    created_at = models.DateTimeField(auto_now_add=True)  # data utworzenia
    updated_at = models.DateTimeField(auto_now=True)  # data modyfikacji

    def __str__(self):
        return self.name

