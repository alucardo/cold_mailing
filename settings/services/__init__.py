"""
Service layer dla operacji na kontach email.
"""

from .smtp_service import test_smtp_connection
from .imap_service import test_imap_connection

__all__ = [
    'test_smtp_connection',
    'test_imap_connection',
]