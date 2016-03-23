from wtforms import Form, BooleanField, StringField, validators, TextAreaField


class JournalForm(Form):

    """Create a form for our learning journal entries."""
    title = StringField('title', [validators.Length(min=1, max=128)])
    text = TextAreaField('text')




class LoginForm(Form):
    """Create login form."""
    username = StringField('username', [validators.length(min=1)])
    password = StringField('password', [validators.length(min=5)])
