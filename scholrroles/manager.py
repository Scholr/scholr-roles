from django.contrib.contenttypes.models import ContentType

from scholrroles import registry
from scholrroles.models import Role, Permission

class PermissionManager(object):
    roles = {}
    _permissions = None

    def __init__(self, user, request = None):
        for role in Role.objects.all():
            role_manager = registry.get_role(role.name)(user,request)
            if role_manager.has_role():
                self.roles[role.name] = role_manager
        self._permissions = Permission.objects.filter(roles__name__in = self.roles.keys()).values_list('pk', flat=True)
    
    @property
    def permissions(self):
        return Permission.objects.filter(pk__in=self._permissions)
    
    def has_role(self, name, obj = None):
        return name in self.roles and self.roles[name].has_role_for(obj)

    def has_perm(self, perm, obj =None):
        try:
            split = perm.split('_')
            app_label, model, perm_name = split[0], split[1], '_'.join(split[2:])
            ctype = ContentType.objects.get_by_natural_key(app_label, model)
            perm = self.permissions.get(name=perm_name, content_type = ctype, instance_perm = obj != None)
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
