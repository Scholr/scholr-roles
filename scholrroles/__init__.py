from django.conf import settings

from scholrroles.behaviour import registry, RoleBehaviour, UserBehaviour
from scholrroles.manager import PermissionManager

def set_permission(user, request):
    user.permissions = PermissionManager(user, request)

    
def initiate_roles(sender, request, **kwargs):
    user = request.user if hasattr(request,'user') else None
    if user:
        user.permissions = set_permission(user, request)

def import_from_string(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

user_behaviour = UserBehaviour
if settings.SCHOLR_ROLES_USER_BEHAVIOUR:
    user_behaviour = import_from_string(settings.SCHOLR_ROLES_USER_BEHAVIOUR)

registry.register(user_behaviour)

def autodiscover():
    """
    Auto-discover INSTALLED_APPS admin.py modules and fail silently when
    not present. This forces an import on them to register any admin bits they
    may want.
    """
    from django.utils.importlib import import_module
    from django.utils.module_loading import module_has_submodule

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        # Attempt to import the app's admin module.

        try:
            import_module('%s.roles' % app)
        except:
            # Decide whether to bubble up this error. If the app just
            # doesn't have an admin module, we can ignore the error
            # attempting to import it, otherwise we want it to bubble up.
            if module_has_submodule(mod, 'roles'):
                raise