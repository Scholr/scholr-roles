# -*- coding: utf-8 -*-
#
# This file is part of Django appschema released under the MIT license.
# See the LICENSE for more information.
from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from django.utils.importlib import import_module
import yaml
import os.path

from scholrroles.models import Role, Permission


class Command(BaseCommand):
    help = 'Creates a new active schema'
    option_list = BaseCommand.option_list + (
        make_option('--file', action='store', dest='role_file',
            default=None, help='Select a file with roles. '
                'Defaults to the settings.ROLE_FILE.'),
    )

    def handle(self, *args, **options):
        files, roles = self.get_roles_files(), []
        print files
        for role_file in files:
            stream = open(role_file, 'r')
            data = yaml.load(stream)
            roles.extend(data['roles'])
            print roles
        self.update_roles(roles)
        
        files = self.get_permission_files()
        for perm_file in files:
            stream = open(perm_file, 'r')
            data = yaml.load(stream)
            self.update_perms(data['perms'])

    def get_roles_files(self):
        files = []
        for app in settings.INSTALLED_APPS:
            module = import_module(app)
            pth = os.path.abspath(module.__path__[0])
            print pth, os.path.isfile(pth + '/roles.yml')
            if os.path.isfile(pth + '/roles.yml'):
                files.append(pth + '/roles.yml')
        return files

    def get_permission_files(self):
        files = []
        for app in settings.INSTALLED_APPS:
            module = import_module(app)
            pth = os.path.abspath(module.__path__[0])
            if os.path.isfile(pth + '/permissions.yml'):
                files.append(pth + '/permissions.yml')
        return files

    def update_roles(self, roles):
        existing_roles = Role.objects.all().values_list('name', flat=True)
        print """
            --------------------
                Create Roles
            --------------------
        """
        for role in roles:
            if role not in existing_roles:
                print role
                Role.objects.create(name = role)

        print """
            --------------------
                Delete Roles
            --------------------
        """
        to_delete = [x for x in existing_roles if x not in roles]
        for role in to_delete:
            print role
        Role.objects.filter(name__in = to_delete).delete()

    def update_perms(self, perms):
        existing_perms = Permission.objects.all()
        for perm in perms:
            existing_perm = existing_perms.filter(content_type=ContentType.objects.get_by_natural_key(perm['app_label'], perm['model']), 
                name = perm['name'], instance_perm = perm['instance_perm'])
            if existing_perm:
                self.update_perm_roles(perm, existing_perm[0])
            else:
                existing_perm = Permission.objects.create(content_type=ContentType.objects.get_by_natural_key(perm['app_label'], perm['model']), 
                    name = perm['name'], instance_perm = perm['instance_perm'])
                print u"    Created Permission: ".format(existing_perm)
                self.update_perm_roles(perm, existing_perm)
    
    def update_perm_roles(self, perm, existing_perm):
        if existing_perm.roles.filter(name__in=perm['roles']).count() < len(perm['roles']):
            print "        Adding roles to: {}".format(existing_perm)
        for role in perm['roles']:
            if not existing_perm.roles.filter(name=role).exists():
                print "            Adding role: {}".format(role)
                existing_perm.roles.add(Role.objects.get(name=role))

        to_delete = existing_perm.roles.exclude(name__in = perm['roles'])
        if to_delete:
            print u"        Deleting roles from: {}, {}".format(existing_perm,to_delete)
            existing_perm.roles.remove(to_delete)


