from django.contrib.contenttypes.models import ContentType

from scholrroles import registry
from scholrroles.models import Role, Permission

class PermissionManager(object):
    roles = {}
    permissions = None

    def __init__(self, request = None):
        for role in Role.objects.all():
            role_manager = registry.get_role(role.name)(request)
            if role_manager.has_role():
                self.roles[role.name] = role_manager
        self.permissions = Permission.objects.filter(roles__name__in = self.roles.keys())

    def has_role(self, name, obj = None):
        return name in self.roles and self.roles[name].has_role_for(obj)

    def has_perm(self, perm, obj =None):
        try:
            app_label, model, perm_name = perm.split('_')
            print app_label, model, perm_name
            ctype = ContentType.objects.get_by_natural_key(app_label, model)
            print ctype
            print self.permissions.filter(content_type = ctype), perm
            perm = self.permissions.get(name=perm, content_type = ctype)
            print 'perm', perm
            if obj:
                for role in perm.roles:
                    print role
                    if self.roles[role].has_role_for(obj):
                        return True
                return False
            else:
                return True
        except:
            return False
