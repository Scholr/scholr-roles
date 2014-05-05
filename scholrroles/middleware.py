from scholrroles.manager import PermissionManager

class PermissionsMiddleware(object):
    def process_request(self, request):
        assert hasattr(request, 'session'), "The Scholr Roles middleware requires session middleware to be installed. Edit your MIDDLEWARE_CLASSES setting to insert 'django.contrib.sessions.middleware.SessionMiddleware'."
        assert hasattr(request, 'user'), "The Scholr Roles middleware requires authentication to be enabled."
        request.user.permissions = request.session.get('permissions', PermissionManager(request))
        print request.user.permissions

