from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import MailingList
from .forms import MailingListForm


def lists_view(request):
    """Lista wszystkich list mailingowych"""
    lists = MailingList.objects.all()
    return render(request, 'mailing_lists/lists.html', {'lists': lists})


def create_list_view(request):
    if request.method == 'POST':
        form = MailingListForm(request.POST)
        if form.is_valid():
            mailing_list = form.save()
            messages.success(request, f'Dodano listę "{mailing_list.name}"')
            return redirect('mailing_lists:lists')
    else:
        form = MailingListForm()

    return render(request, 'mailing_lists/create_list.html', {'form': form})


def edit_list_view(request, pk):
    mailing_list = get_object_or_404(MailingList, pk=pk)

    if request.method == 'POST':
        form = MailingListForm(request.POST, instance=mailing_list)
        if form.is_valid():
            form.save()
            messages.success(request, f'Zaktualizowano "{mailing_list.name}"')
            return redirect('mailing_lists:lists')
    else:
        form = MailingListForm(instance=mailing_list)

    return render(request, 'mailing_lists/edit_list.html', {
        'form': form,
        'mailing_list': mailing_list
    })


def delete_list_view(request, pk):
    mailing_list = get_object_or_404(MailingList, pk=pk)

    if request.method == 'POST':
        name = mailing_list.name
        mailing_list.delete()
        messages.success(request, f'Usunięto listę "{name}"')

    return redirect('mailing_lists:lists')