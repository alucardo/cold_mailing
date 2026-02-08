from django.http import HttpResponseRedirect
from django.shortcuts import render
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
            return HttpResponseRedirect('/settings/apis')
    else:
        form = CreateApiForm()
    return render(request, 'settings/create_api.html', {'form': form})