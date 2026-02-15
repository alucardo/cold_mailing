from django.urls import path
from . import views

app_name = 'mailing_lists'

urlpatterns = [
    path('', views.lists_view, name='lists'),
    path('create/', views.create_list_view, name='create_list'),
    path('edit/<int:pk>/', views.edit_list_view, name='edit_list'),
    path('delete/<int:pk>/', views.delete_list_view, name='delete_list'),
]