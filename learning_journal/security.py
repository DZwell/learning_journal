from __future__ import unicode_literals
from wtforms.csrf.core import CSRF
from hashlib import md5
from pyramid.security import Allow, Everyone, Authenticated, ALL_PERMISSIONS
from passlib.apps import custom_app_context as pwd_context
from wtforms.ext.csrf import SecureForm
import os


SECRET_KEY = 'shhhhh'


class SecureAssForm(SecureForm):

    def generate_token(self, csrf_context):
        token = md5(SECRET_KEY + csrf_context).hexdigest()
        return token

    def validate_token(self, form, field):
        if field.data != field.current_token:
            raise ValueError('Invalid CSRF')



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
