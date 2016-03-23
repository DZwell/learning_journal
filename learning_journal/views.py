from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from .form import JournalForm, LoginForm
from sqlalchemy.exc import DBAPIError
from sqlalchemy import desc
import transaction
import markdown

from .models import (
    DBSession,
    Entry,
    )


# @view_config(route_name='login_view', renderer='string')
# def login_view(request):
#     form = LoginForm(request.POST)
#     if request.method == 'POST':
#         username = requ



@view_config(route_name='home', renderer='templates/list_view.jinja2', permission='user')
def list_view(request):
    """Handle the view of our home page."""
    return {'entries': DBSession.query(Entry).order_by(desc(Entry.created)).all()}


@view_config(route_name='detail_view', renderer='templates/detail_view.jinja2')
def detail_view(request):
    """Handle the view of a single journaly entry."""
    md = markdown.Markdown(safe_mode='replace', html_replacement_text='NO')
    this_id = request.matchdict['this_id']
    entry = DBSession.query(Entry).get(this_id)
    text = md.convert(entry.text)
    return {'entry': entry, 'text': text}


@view_config(route_name='add_view', renderer='templates/add_view.jinja2')
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


@view_config(route_name='edit_view', renderer='templates/add_view.jinja2')
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
