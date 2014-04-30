from collections import defaultdict
from .utils import get_value_from_accessor

class RoleBehaviour(object):
    ids = []
    object_accessors = {}
    def has_role(self, user, request):
        return True

    def has_role_for(self, obj):
        if self.ids:
            if obj._meta.object_name in self.object_accessors:
                return get_value_from_accessor(obj, self.object_accessors[obj._meta.object_name]) in self.ids
        return True 



def role_behaviour_factory():
    return RoleBehaviour()
    
class RoleBehaviourRegistry(object):
    _registry = defaultdict(role_behaviour_factory)
    def register(self, cls):
        self._registry[cls.role] = cls

    def get_role(self, role):
        return self._registry[role]

registry = RoleBehaviourRegistry()