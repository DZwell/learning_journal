# -*- coding: utf-8 -*-
import os
import pytest
from sqlalchemy import create_engine
from learning_journal.models import DBSession, Base

from pyramid.paster import get_appsettings
from webtest import TestApp
from learning_journal import main



TEST_DATABASE_URL = os.environ.get('TESTDB_URL')


@pytest.fixture(scope='session')
def sqlengine(request):
    engine = create_engine(TEST_DATABASE_URL)
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)

    def teardown():
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return engine

@pytest.fixture()
def dbtransaction(request, sqlengine):
    connection = sqlengine.connect()
    transaction = connection.begin()
    DBSession.configure(bind=connection)

    def teardown():
        transaction.rollback()
        connection.close()
        DBSession.remove()

    request.addfinalizer(teardown)

    return connection


@pytest.fixture()
def dummy_post(dbtransaction):
    from pyramid.testing import DummyRequest
    from webob.multidict import MultiDict
    req = DummyRequest()
    req.method = 'POST'
    md = MultiDict()
    md.add('title', 'dummy title')
    md.add('text', 'dummy text')
    req.POST = md
    return req


@pytest.fixture()
def app(config_path, dbtransaction, test_url):
    """Create pretend app fixture of main app to test routing."""
    settings = get_appsettings(config_path)
    settings['sqlalchemy.url'] = test_url
    app = main({}, **settings)
    return TestApp(app)
