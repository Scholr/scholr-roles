from django.contrib.contenttypes.models import ContentType

from scholrroles import registry
from scholrroles.models import Role, Permission

class PermissionManager(object):
    roles = {}
    permissions = None

    def __init__(self, request = None):
        print 'teste 1 2'
        for role in Role.objects.all():
            role_manager = registry.get_role(role.name)(request)
            print role_manager.has_role()
            if role_manager.has_role():
                self.roles[role.name] = role_manager
        print self.roles.keys()
        self.permissions = Permission.objects.filter(roles__name__in = self.roles.keys())

    def has_role(self, name, obj = None):
        return name in self.roles and self.roles[name].has_role_for(obj)

    def has_perm(self, perm, obj =None):
        try:
            app_label, model, perm_name = perm.split('_')
            ctype = ContentType.objects.get_by_natural_key(app_label, model)
            perm = self.permissions.get(name=perm_name, content_type = ctype, instance_perm = obj != None)
            print 'perm', perm
            if obj:
                for role in perm.roles:
                    print role
                    if self.roles[role].has_role_for(obj):
                        return True
                return False
            else:
                return True
        except Exception as e:
            print perm, obj, e
            return False
