# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pyramid.security import Allow, Everyone, Authenticated, ALL_PERMISSIONS


class DefaultRoot(object):
    __acl__ = [
        (Allow, Authenticated, 'view')
    ]

    def __init__(self, request):
        """Take request from view, pass it to Default root to check permissions."""
        self.request = request
