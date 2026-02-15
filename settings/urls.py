from django.urls import path
from . import views

app_name = 'settings'
urlpatterns = [
    path('', views.home, name='home'),
    # ---- Klucze API ----
    path('apis/', views.apis_view, name='list_apis'),
    path('apis/create/', views.create_api_view, name='create_api'),
    path('apis/edit/<int:pk>/', views.edit_api_view, name='edit_api'),
    path('apis/delete/<int:pk>/', views.delete_api_view, name='delete_api'),

    # ---- Cold email accounts ----
    path('email-accounts/', views.email_accounts_view, name='email_accounts'),
    path('email-accounts/create/', views.create_email_account_view, name='create_email_account'),
    path('email-accounts/edit/<int:pk>/', views.edit_email_account_view, name='edit_email_account'),
    path('email-accounts/delete/<int:pk>/', views.delete_email_account_view, name='delete_email_account'),
]