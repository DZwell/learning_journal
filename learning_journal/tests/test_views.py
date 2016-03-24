# -*- coding: utf-8 -*-
import os
from pyramid.testing import DummyRequest
from learning_journal.models import Entry, DBSession
from webtest.app import AppError
import pytest

from learning_journal.views import (
    list_view,
    detail_view,
    add_view,
    edit_view
)


def test_no_access_to_view(app):
    response = app.get('/', status='4*')
    assert response.status_code == 403


def test_access_to_view(authenticated_app):
    response = authenticated_app.get('/')
    assert response.status_code == 200



