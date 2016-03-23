# -*- coding: utf-8 -*-
import os
import pytest
from sqlalchemy import create_engine
from learning_journal.models import DBSession, Base
from learning_journal import main
import webtest


TESTDB_URL = os.environ.get('TESTDB_URL')


@pytest.fixture(scope='session')
def sqlengine(request):
    """Takes care of connection to DB."""
    engine = create_engine(TESTDB_URL)
    Base.metadata.create_all(engine)
    connection = engine.connect()
    DBSession.configure(bind=connection)

    def teardown():
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return connection


@pytest.fixture()
def DB_connection_for_tests(request, sqlengine):
    """Undoes stuff in DB from other DB tests."""
    from transaction import abort
    connection = sqlengine
    transaction = connection.begin()
    request.addfinalizer(transaction.rollback)
    request.addfinalizer(abort)


@pytest.fixture()
def app(DB_connection_for_tests):
    from pyramid.paster import get_appsettings
    settings = get_appsettings('daniel_development.ini')
    settings = {'sqlalchemy.url': TESTDB_URL}
    app = main({}, **settings)
    return webtest.TestApp(app)
