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
                return redirect('mailing_lists:show_list', pk=list_pk)
    else:
        form = ContactForm(mailing_list=mailing_list)

    return render(request, 'mailing_lists/create_contact.html', {
        'form': form,
        'mailing_list': mailing_list
    })


def edit_contact_view(request, list_pk, contact_pk):
    """Edycja kontaktu w liście mailingowej"""
    mailing_list = get_object_or_404(MailingList, pk=list_pk)
    contact = get_object_or_404(Contact, pk=contact_pk, mailing_list=mailing_list)

    if request.method == 'POST':
        form = ContactForm(
            request.POST,
            instance=contact,
            mailing_list=mailing_list,
            hide_status=False  # ← Pokaż pole status przy edycji!
        )

        if form.is_valid():
            form.save()
            messages.success(request, f'Zaktualizowano kontakt {contact.email}')
            return redirect('mailing_lists:show_list', pk=list_pk)
    else:
        form = ContactForm(
            instance=contact,
            mailing_list=mailing_list,
            hide_status=False  # ← Tutaj też!
        )

    return render(request, 'mailing_lists/edit_contact.html', {
        'form': form,
        'contact': contact,
        'mailing_list': mailing_list
    })

def delete_contact_view(request, list_pk, contact_pk):
    """Usuwanie kontaktu z listy mailingowej"""
    mailing_list = get_object_or_404(MailingList, pk=list_pk)
    contact = get_object_or_404(Contact, pk=contact_pk, mailing_list=mailing_list)

    if request.method == 'POST':
        email = contact.email
        contact.delete()
        messages.success(request, f'Usunięto kontakt {email}')

    return redirect('mailing_lists:show_list', pk=list_pk)