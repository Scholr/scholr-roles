from scholrroles.manager import PermissionManager

class PermissionsMiddleware(object):
    def process_request(self, request):
        assert hasattr(request, 'session'), "The Scholr Roles middleware requires session middleware to be installed. Edit your MIDDLEWARE_CLASSES setting to insert 'django.contrib.sessions.middleware.SessionMiddleware'."
        permissions = request.session.get('permissions',None)
        print 'PMiddleware', permissions.roles if permissions else None
        if hasattr(request, 'user') and not hasattr(request.user,'permissions') :
            print request.session.get('permissions',None)
            request.user.permissions = request.session.get('permissions', None)

