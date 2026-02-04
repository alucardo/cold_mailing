from django.shortcuts import render

# Create your views here.
def apis(request):
    return render(request, 'settings/apis.html')