# -*- coding: utf-8 -*-
from learning_journal.models import Entry, DBSession

def test_create_entry(sqlengine):
    """Assert entry was entered into database."""
    new_entry = Entry(title="Entry1", text="Hey, this works. Awesome.")
    assert new_entry.id is None
    DBSession.add(new_entry)
    DBSession.flush()
    assert new_entry.id is not None
