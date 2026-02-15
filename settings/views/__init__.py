from .general_views import (
    home,
)

from .api_key_views import (
    apis_view,
    create_api_view,
    edit_api_view,
    delete_api_view,
)

from .email_account_views import (
    email_accounts_view,
    create_email_account_view,
    show_email_account_view,
    edit_email_account_view,
    delete_email_account_view,
)

__all__ = [
    'home',
    'apis_view',
    'create_api_view',
    'edit_api_view',
    'delete_api_view',
    'email_accounts_view',
    'create_email_account_view',
    'show_email_account_view',
    'edit_email_account_view',
    'delete_email_account_view',
]