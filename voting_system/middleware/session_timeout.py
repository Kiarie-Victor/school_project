import datetime
from django.conf import settings
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib.auth import logout


class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.TIMEOUT = getattr(settings, 'AUTO_LOGOUT_DELAY', 15)  # in minutes

    def __call__(self, request):
        if not request.user.is_authenticated:
            return self.get_response(request)

        now = timezone.now()

        last_activity = request.session.get('last_activity')
        if last_activity:
            try:
                last_activity = datetime.datetime.fromisoformat(last_activity)
                
                if timezone.is_naive(last_activity):
                    last_activity = timezone.make_aware(last_activity)
            except (ValueError, TypeError):
                last_activity = now

            if (now - last_activity).total_seconds() > self.TIMEOUT * 60:
                logout(request)
                return redirect('accounts/login')

        request.session['last_activity'] = now.isoformat()

        return self.get_response(request)
