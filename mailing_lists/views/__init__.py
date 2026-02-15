"""
Widoki dla aplikacji mailing_lists.
Zorganizowane w osobne moduły dla lepszej czytelności.
"""

# Widoki dla list mailingowych
from .list_views import (
    lists_view,
    show_list_view,
    create_list_view,
    edit_list_view,
    delete_list_view,
)

# Widoki dla kontaktów
from .contact_views import (
    create_contact_view,
    edit_contact_view,
    delete_contact_view,
)

# To pozwala importować: from mailing_lists.views import lists_view
__all__ = [
    'lists_view',
    'show_list_view',
    'create_list_view',
    'edit_list_view',
    'delete_list_view',
    'create_contact_view',
    'edit_contact_view',
    'delete_contact_view',
]