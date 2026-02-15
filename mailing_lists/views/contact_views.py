from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..models import MailingList, Contact
from ..forms import ContactForm


def create_contact_view(request, list_pk):
    """Dodawanie kontaktu do listy mailingowej"""
    mailing_list = get_object_or_404(MailingList, pk=list_pk)

    if request.method == 'POST':
        form = ContactForm(request.POST, mailing_list=mailing_list)

        if form.is_valid():
            contact = form.save(commit=False)
            contact.mailing_list = mailing_list
            contact.status = 'active'
            contact.save()

            messages.success(request, f'Dodano kontakt {contact.email}')

            if 'save_and_continue' in request.POST:
                # Zapisz i dodaj następny
                return redirect('mailing_lists:create_contact', list_pk=list_pk)
            else:
                # Zapisz i wróć do listy
                return redirect('mailing_lists:list_detail', pk=list_pk)
    else:
        form = ContactForm(mailing_list=mailing_list)

    return render(request, 'mailing_lists/create_contact.html', {
        'form': form,
        'mailing_list': mailing_list
    })