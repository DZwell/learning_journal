from pyramid.response import Response
from pyramid.view import view_config
from pyramid.security import remember, forget, ALL_PERMISSIONS
from pyramid.httpexceptions import HTTPFound
from .security import DefaultRoot, check_password
from passlib.apps import custom_app_context as pwd_context
from .form import JournalForm, LoginForm
from sqlalchemy.exc import DBAPIError
from sqlalchemy import desc
import transaction
import markdown
import os

from .models import (
    DBSession,
    Entry,
    )

#Must source bash_profile in terminal tab where server is run
USER_NAME = os.environ.get('USER_NAME')
PASSWORD = os.environ.get('PASSWORD')



@view_config(route_name='login_view', renderer='templates/login.jinja2')
def login_view(request):
    # import pdb; pdb.set_trace()
    context = get_auth_tkt_from_request(request)
    form = LoginForm(request.POST, csrf_context=context)
    if request.method == 'POST' and form.validate():
        #'' is default val. if not username, return '' instead of throw error
        username = request.params.get('username', '')
        password = request.params.get('password', '')
        if check_password(password):
            #remember takes request and whatever else you want included in that request
            headers = remember(request, username)
            # csrf_token = request.session.get_csrf_token()
            return HTTPFound(location='/', headers=headers)
    return {}


@view_config(route_name='logout_view')
def logout_view(request):
    headers = forget(request)
    return HTTPFound(location='/login', headers=headers)



@view_config(route_name='home', renderer='templates/list_view.jinja2', permission='view')
def list_view(request):
    """Handle the view of our home page."""
    return {'entries': DBSession.query(Entry).order_by(desc(Entry.created)).all()}


@view_config(route_name='detail_view', renderer='templates/detail_view.jinja2', permission='view')
def detail_view(request):
    """Handle the view of a single journaly entry."""
    md = markdown.Markdown(safe_mode='replace', html_replacement_text='NO')
    this_id = request.matchdict['this_id']
    entry = DBSession.query(Entry).get(this_id)
    text = md.convert(entry.text)
    return {'entry': entry, 'text': text}


@view_config(route_name='add_view', renderer='templates/add_view.jinja2', permission='add')
def add_view(request):
    """Handle the view of our adding new entry page."""
    form = JournalForm(request.POST)
    if request.method == "POST" and form.validate():
        new_entry = Entry(title=form.title.data, text=form.text.data)
        DBSession.add(new_entry)
        DBSession.flush()
        this_id = new_entry.id
        return HTTPFound(location='/detail/{}'.format(this_id))
    return {'form': form}




@view_config(route_name='edit_view', renderer='templates/edit_view.jinja2', permission='edit')
def edit_view(request):
    """Handle the view of our edit entry page."""
    this_id = request.matchdict['this_id']
    entry = DBSession.query(Entry).get(this_id)
    form = JournalForm(request.POST, entry)
    if request.method == 'POST' and form.validate():
        form.populate_obj(entry)
        this_id = entry.id
        return HTTPFound(location='/detail/{}'.format(this_id))
    return {'form': form}



def get_auth_tkt_from_request(request):
    """Get an auth_tkt from a request."""
    request_cookies = request.headers.items()
    auth_tkts = [value for cookie, value in request_cookies
                 if cookie == 'Cookie' and value.startswith('auth_tkt')]
    if not auth_tkts:
        return ''
    return auth_tkts[0]


conn_err_msg = """
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_learning_journal_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
