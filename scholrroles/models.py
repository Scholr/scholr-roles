from django.db import models
from django.contrib.contenttypes.models import ContentType
from scholrroles.behaviour import registry

class Role(models.Model):
    _behaviour = None
    name = models.CharField(max_length=255)
    @property
    def behaviour(self):
        if self._behaviour:
            return self._behaviour
        self._behaviour = registry.get_role(self.name)
   
    def __unicode__(self):
        return u'{}'.format(self.name)



class Permission(models.Model):
    content_type = models.ForeignKey(ContentType, related_name="permissions")
    name = models.CharField(max_length=255)
    instance_perm = models.BooleanField(default=False)
    roles = models.ManyToManyField(Role)

    def __unicode__(self):
        return u'{} {}'.format(self.name, 'model' if not self.instance_perm else 'instance')

