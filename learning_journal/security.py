# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pyramid.security import Allow, Everyone, Authenticated, ALL_PERMISSIONS
from passlib.apps import custom_app_context as pwd_context
import os



class DefaultRoot(object):
    __acl__ = [
        (Allow, Authenticated, 'view')
    ]

    def __init__(self, request):
        """Take request from view, pass it to Default root to check permissions."""
        self.request = request


def check_password(password):
    """Varify password matches hashed password."""
    hashed = pwd_context.encrypt(os.environ.get('PASSWORD'))
    return pwd_context.verify(password, hashed)
