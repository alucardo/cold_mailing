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

from .footer_views import (
    list_footers_view,
    create_footer_view,
    edit_footer_view,
    delete_footer_view,
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
    'list_footers_view',
    'create_footer_view',
    'edit_footer_view',
    'delete_footer_view',
]