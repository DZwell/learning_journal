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


def test_access_to_view(app):
    response = app.get('/')
    assert response.status_code == 200


def test_no_access_to_view(app):
    with pytest.raises(AppError):
        app.get('/')
