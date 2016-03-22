import datetime
import psycopg2
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    Unicode,
    UnicodeText,
    ForeignKey,
    )
from pyramid.security import Allow, Everyone
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    )
from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Entry(Base):
    """Our Journal Entry class."""

    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(128), unique=True)
    text = Column(UnicodeText)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    author_id = Column(Integer, ForeignKey('users.id'))
    #Ties User model to Entry model
    author = relationship('User', back_populates='entries')

    @property
    def __acl__(self):
        """Add permissions for specific instance of Entry object.
        self.author.username is the user who created this Entry instance.
        """
        return [
            (Allow, Everyone, 'view'),
            (Allow, self.author.username, 'edit')
        ]
