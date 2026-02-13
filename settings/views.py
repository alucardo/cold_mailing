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
            api = ApiSetting(
                name = form.cleaned_data['name'],
                text = form.cleaned_data['text'],
                api_type_id = 1
            )
            api.save()
            return redirect('settings:list_apis')
    else:
        form = CreateApiForm()
    return render(request, 'settings/create_api.html', {'form': form})

def delete_api_view(request, pk):
    api_setting = get_object_or_404(ApiSetting, pk=pk)
    if request.method == 'POST':
        api_setting.delete()
        messages.success(request, f'Usunięto {api_setting.name}')
    return redirect('settings:list_apis')