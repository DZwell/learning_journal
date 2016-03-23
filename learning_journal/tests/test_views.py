# -*- coding: utf-8 -*-
from pyramid.testing import DummyRequest
from learning_journal.models import Entry, DBSession
import pytest
from learning_journal import main
import webtest
from learning_journal.views import (
    list_view,
    detail_view,
    add_view,
    edit_view
)


@pytest.fixture()
def app():
    settings = {'sqlalchemy.url': 'postgres://danielzwelling:@localhost:5432/learning_journal'}
    app = main({}, **settings)
    return webtest.TestApp(app)



def test_access_to_view(app):
    response = app.get('/login')
    assert response.status_code == 200


def test_no_access_to_view(app):
    response = app.get('/login')
    assert response.status_code == 403
