from django.contrib.contenttypes.models import ContentType

from scholrroles import registry
from scholrroles.models import Role, Permission

class PermissionManager(object):
    roles = {}
    _permissions = []

    def __init__(self, request = None):
        for role in Role.objects.all():
            role_manager = registry.get_role(role.name)(request)
            if role_manager.has_role():
                self.roles[role.name] = role_manager
        self._permissions = list(Permission.objects.filter(roles__name__in = self.roles.keys()).values_list('pk', flat=True))

    def has_role(self, name, obj = None):
        return name in self.roles and self.roles[name].has_role_for(obj)

    def get_permissions(self):
        return Permission.objects.filter(pk__in = self._permissions)
    def has_perm(self, perm, obj =None):
        try:
            permissions = self.get_permissions()
            print self.roles.keys()
            split = perm.split('_')
            app_label, model, perm_name = split[0], split[1], '_'.join(split[2:])
            print app_label, model, perm_name
            ctype = ContentType.objects.get_by_natural_key(app_label, model)
            perm = permissions.get(name=perm_name, content_type = ctype, instance_perm = obj != None)
            if obj:
                for role in perm.roles.all():
                    if role.name in self.roles and self.roles[role.name].has_role_for(obj):
                        return True
                return False
            else:
                return True
        except Exception as e:
            print perm, obj, e
            return False
