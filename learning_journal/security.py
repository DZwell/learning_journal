# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pyramid.security import Allow, Everyone
from pyramid.security import ALL_PERMISSIONS


class DefaultRoot(object):
    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, 'g:admins', ALL_PERMISSIONS)
    ]


