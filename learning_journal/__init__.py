from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory
from sqlalchemy import engine_from_config
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from .security import DefaultRoot
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
    """This function returns a Pyramid WSGI application."""
    if 'DATABASE_URL' in os.environ:
        settings['sqlalchemy.url'] = os.environ['DATABASE_URL']
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings, root_factory=DefaultRoot)
    secret = os.environ.get('AUTH_SECRET', 'somesecret')
    authN = AuthTktAuthenticationPolicy('afd', hashalg='sha512')
    authZ = ACLAuthorizationPolicy()
    config.set_authentication_policy(authN)
    config.set_authorization_policy(authZ)
    session_factory = SignedCookieSessionFactory('itsaseekrit')
    config.set_session_factory(session_factory)
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/list')
    config.add_route('detail_view', '/detail/{this_id}')
    config.add_route('login_view', '/')
    config.add_route('logout_view', '/logout')
    config.add_route('add_view', '/add')
    config.add_route('edit_view', '/edit/{this_id}')
    config.scan()
    return config.make_wsgi_app()
