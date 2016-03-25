from wtforms import Form, BooleanField, StringField, validators, TextAreaField
from .security import SecureAssForm


class JournalForm(SecureAssForm):

    """Create a form for our learning journal entries."""
    title = StringField('title', [validators.Length(min=1, max=128)])
    text = TextAreaField('text')




class LoginForm(SecureAssForm):
    """Create login form."""
    username = StringField('username', [validators.length(min=1)])
    password = StringField('password', [validators.length(min=5)])
