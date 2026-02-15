from django.urls import path
from . import views

app_name = 'mailing_lists'

urlpatterns = [
    # ---- Listy mailingowe ----
    path('', views.lists_view, name='lists'),
    path('<int:pk>', views.show_list_view, name='show_list'),
    path('create/', views.create_list_view, name='create_list'),
    path('edit/<int:pk>/', views.edit_list_view, name='edit_list'),
    path('delete/<int:pk>/', views.delete_list_view, name='delete_list'),

    # ---- Adresy e-mail na liście ----
    path('<int:list_pk>/contacts/create/', views.create_contact_view, name='create_contact'),
    path('<int:list_pk>/contacts/<int:contact_pk>/edit/', views.edit_contact_view, name='edit_contact'),

    path('<int:list_pk>/contacts/<int:contact_pk>/delete/', views.delete_contact_view, name='delete_contact'),

]