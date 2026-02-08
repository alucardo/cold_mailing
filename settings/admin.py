from django.contrib import admin
from .models import ApiSetting, ApiType

# Register your models here.

class ApiTypeAdmin(admin.ModelAdmin):
    pass

class ApiSettingAdmin(admin.ModelAdmin):
    list_display = ['name', 'api_type', 'created_at']

admin.site.register(ApiType, ApiTypeAdmin)
admin.site.register(ApiSetting, ApiSettingAdmin)