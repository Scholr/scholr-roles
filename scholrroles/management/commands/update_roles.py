# -*- coding: utf-8 -*-
#
# This file is part of Django appschema released under the MIT license.
# See the LICENSE for more information.
from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand
import yaml
from scholrroles.models import Role, Permission
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = 'Creates a new active schema'
    option_list = BaseCommand.option_list + (
        make_option('--file', action='store', dest='role_file',
            default=None, help='Select a file with roles. '
                'Defaults to the settings.ROLE_FILE.'),
    )

    def handle(self, *args, **options):
        file = options.get('role_file', settings.ROLES_FILE)
        stream = open(file, 'r')
        data = yaml.load(stream)
        print data
        #self.update_roles(data['roles'])
        #self.update_perms(data['perms'])

    def update_roles(self, roles):
        existing_roles = Role.objects.all().values_list('name', flat=True)
        for role in roles:
            if role not in existing_roles:
                Role.objects.create(name = role)

        to_delete = [x for x in existing_roles if x not in roles]
        Role.objects.filter(name__in = to_delete).delete()

    def update_perms(self, perms):
        existing_perms = Permission.objects.all()
        for perm in perms:
            existing_perm = existing_perms.filter(content_type=ContentType.objects.get_by_natural_key(perm.app_label, perm.model), name = perm.name, instance_perm = perm.instance_perm)
            if existing_perm:
                existing_perm = existing_perm[0]




        