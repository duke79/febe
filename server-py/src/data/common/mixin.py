from sqlalchemy import Column, Integer, Text, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm.exc import NoResultFound

from . import db_session, DBType, db_type
# from flask_sqlalchemy import Model
from ...core.traces import print_exception_traces


class Mixin(object):
    """
    ref: https://chase-seibert.github.io/blog/2016/03/31/flask-sqlalchemy-sessionless.html
    """

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    if db_type == DBType.sqlite:
        json_data = Column(Text, nullable=True)
    if db_type == DBType.mysql:
        json_data = Column(Text, nullable=True)
    if db_type == DBType.postgres:
        json_data = Column(JSONB, nullable=True)

    # https://stackoverflow.com/a/12155686/973425
    created_at = Column(DateTime, nullable=False,
                        server_default=func.now())
    updated_at = Column(DateTime, nullable=False,
                        server_default=func.now(),
                        server_onupdate=func.now())

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def create(self, **kwargs):
        return self.update(**kwargs)

    def save(self):
        setattr(self, "updated_at", func.now())  # server_onupdate failing for postgres

        session = db_session()
        local_object = session.merge(self)
        session.add(local_object)
        # try:
        self._flush()
        session.commit()
        # except DatabaseError as e:
        #     code = e.orig.args[0]
        #     if code == 1062:
        #         raise
        #     return code
        session.connection().close()
        return local_object

    def find(self, **kwargs):
        rows = self.session().query(self.__class__)
        for attr, value in kwargs.items():
            rows.filter(getattr(self, attr) == value)
        res = rows.all()
        if res:
            return res
        else:
            raise NoResultFound

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return self.save()

    def delete(self):
        session = db_session()
        local_object = session.merge(self)  # https://stackoverflow.com/a/47663833/973425
        session.delete(local_object)
        self._flush()
        session.commit()

    def _flush(self):
        session = db_session()
        try:
            session.flush()
        # db_session.refresh(self)
        except DatabaseError as e:
            session.rollback()
            print_exception_traces(e)
            raise

    @staticmethod
    def session():
        return db_session()
