#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import tuple_

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a user to the database
        """
        if not email or not hashed_password:
            return None
        try:
            user = User(email=email, hashed_password=hashed_password)
            self._session.add(user)
            self._session.commit()
            return user
        except Exception:
            self._session.rollback()
            return None

    def find_user_by(self, **kwargs) -> User:
        """Find a user by a given keyword argument
        """
        if not kwargs:
            raise InvalidRequestError()

        for key in kwargs:
            if not hasattr(User, key):
                raise InvalidRequestError()

        keys, values = zip(*kwargs.items())
        result = self._session.query(User).filter(
            tuple_(*keys).in_([tuple(values)])
        ).first()

        if result is None:
            raise NoResultFound()
        return result

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user by a given keyword argument
        """
        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            return
        for key, value in kwargs.items():
            if not hasattr(User, key):
                raise ValueError()
            setattr(user, key, value)
        self._session.commit()
