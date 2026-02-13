from django.urls import path
from . import views

app_name = 'settings'
urlpatterns = [
    path('apis/', views.apis_view, name='list_apis'),
    path('apis/create/', views.create_api_view, name='create_api'),
    path('apis/delete/<int:pk>/', views.delete_api_view, name='delete_api'),
]