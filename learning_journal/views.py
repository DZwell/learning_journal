from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from .form import JournalForm
from sqlalchemy.exc import DBAPIError
import transaction
from pyramid.security import remember, forget

from .models import (
    DBSession,
    Entry,
    )



@view_config(route_name='login', renderer='string')
def login_view(request):
    headers = remember(request, userid='daniel')
    return HTTPFound(location='/', headers=headers)
    #Will add CSRF stuff later


@view_config(route_name='logout', renderer='string')
def logout_view(request):
    headers = forget(request)
    return HTTPFound(location='/', headers=headers)



@view_config(route_name='home', renderer='templates/list_view.jinja2', permission='view')
def list_view(request):
    """Handle the view of our home page."""
    return {'entries': DBSession.query(Entry).all()}


@view_config(route_name='detail_view', renderer='templates/detail_view.jinja2', permission='view')
def detail_view(request):
    """Handle the view of a single journaly entry."""
    this_id = request.matchdict['this_id']
    entry = DBSession.query(Entry).filter(Entry.id == this_id).first()
    return {'entry': entry}


@view_config(route_name='add_view', renderer='templates/add_view.jinja2', permission='add')
def add_view(request):
    """Handle the view of our adding new entry page."""
    form = JournalForm(request.POST)
    if request.method == "POST" and form.validate():
        new_entry = Entry(title=form.title.data, text=form.text.data)
        DBSession.add(new_entry)
        DBSession.flush()
        this_id = new_entry.id
        transaction.commit()
        raise HTTPFound(location='/detail/{}'.format(this_id))
    return {'form': form}




@view_config(route_name='edit_view', renderer='templates/edit_view.jinja2', permission='edit')
def edit_view(request):
    """Handle the view of our edit entry page."""
    pass



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
