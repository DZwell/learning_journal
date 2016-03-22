from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.authentication import AuthTktAuthenticationPolicy
import os

from .models import (
    DBSession,
    Base,
    )


def make_session(settings):
    from sqlalchemy.orm import sessionmaker
    engine = engine_from_config(settings, 'sqlalchemy')
    Session = sessionmaker(bind=engine)
    return Session()

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine


    #authentication
    dummy_auth = os.environ.get(JOURNAL_AUTH_SECRET, 'testvalue')
    authentication_policy = AuthTktAuthenticationPolicy(
        secret= dummy_auth,
        hashalg='sha512',
        callback='userfinder',
    )

    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('detail_view', '/detail/{this_id}')

    config.add_route('add_view', '/add')
    config.add_route('edit_view', '/detail/{this_id}/edit')
    config.scan()
    return config.make_wsgi_app()
