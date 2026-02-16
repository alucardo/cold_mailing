"""
Custom middleware dla projektu.
"""

from django.shortcuts import redirect
from django.conf import settings


class LoginRequiredMiddleware:
    """
    Middleware wymuszający logowanie dla wszystkich stron oprócz whitelisty.

    Publiczne URLe (nie wymagają logowania):
    - Strona główna (/)
    - Logowanie/rejestracja (/accounts/*)
    - Admin login
    - Pliki statyczne
    """

    def __init__(self, get_response):
        self.get_response = get_response

        # Prefiksy URL które NIE wymagają logowania
        self.exempt_paths = [
            '/',  # Strona główna
            '/accounts/login/',  # Logowanie
            '/accounts/register/',  # Rejestracja
            '/accounts/logout/',  # Wylogowanie
            '/admin/login/',  # Admin login
            '/static/',  # Pliki statyczne
            '/media/',  # Pliki media
        ]

    def __call__(self, request):
        # Sprawdź czy user jest zalogowany
        if not request.user.is_authenticated:
            path = request.path

            # Sprawdź czy URL jest w whiteliście
            if not self._is_exempt(path):
                # Przekieruj na login z 'next' parametrem
                login_url = settings.LOGIN_URL
                return redirect(f'{login_url}?next={path}')

        response = self.get_response(request)
        return response

    def _is_exempt(self, path):
        """Sprawdza czy ścieżka jest zwolniona z wymogu logowania"""

        # Dokładne dopasowanie dla '/'
        if path == '/':
            return True

        # Dopasowanie po prefiksie dla reszty
        for exempt_path in self.exempt_paths:
            if exempt_path != '/' and path.startswith(exempt_path):
                return True

        return False