from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import ApiType, ApiSetting
from .forms import CreateApiForm

# Create your views here.
def apis_view(request):
    api_list = ApiSetting.objects.all()
    context = {'api_list': api_list}
    return render(request, 'settings/apis.html', context)

def create_api_view(request):
    if request.method == 'POST':
        form = CreateApiForm(request.POST)
        if form.is_valid():
            api = form.save()
            messages.success(request, f'Dodano {api.name}')
            return redirect('settings:list_apis')
    else:
        form = CreateApiForm()
    return render(request, 'settings/create_api.html', {'form': form})


def edit_api_view(request, pk):
    api_setting = get_object_or_404(ApiSetting, pk=pk)

    if request.method == 'POST':
        form = CreateApiForm(request.POST, instance=api_setting)
        if form.is_valid():
            form.save()
            messages.success(request, f'Zaktualizowano {api_setting.name}')
            return redirect('settings:list_apis')
    else:
        form = CreateApiForm(instance=api_setting)

    return render(request, 'settings/edit_api.html', {'form': form, 'api': api_setting})


def delete_api_view(request, pk):
    api_setting = get_object_or_404(ApiSetting, pk=pk)
    if request.method == 'POST':
        api_setting.delete()
        messages.success(request, f'Usunięto {api_setting.name}')
    return redirect('settings:list_apis')