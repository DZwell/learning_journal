# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pyramid.security import Allow, Everyone
from pyramid.security import ALL_PERMISSIONS


class DefaultRoot(object):
    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, 'g:admins', ALL_PERMISSIONS)
    ]

    def __init__(self, request):
        self.request = request


def userfinder(user, request):
    """Return either list of users or None."""
    users = []
    if user.lower() in request.admins:
        user.append('g:admins')
    return users or None


