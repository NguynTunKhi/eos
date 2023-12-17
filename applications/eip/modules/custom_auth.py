# -*- coding: utf-8 -*-

from gluon import tools

class CustomAuth(tools.Auth):
    def has_permission(self,
                       name='any',
                       table_name='',
                       record_id=0,
                       user_id=None,
                       group_id=None):
        if self.has_membership('admin'):
            return True
        return super(CustomAuth, self).has_permission(name=name, table_name=table_name, record_id=record_id, user_id=user_id, group_id=group_id)

    def check_has_permission_for_manager(self, allowed_permissions, table_name, name):
        if self.has_membership('admin'):
            return True
        if allowed_permissions.has_key(table_name):
            if name in allowed_permissions[table_name]:
                return True
        return False