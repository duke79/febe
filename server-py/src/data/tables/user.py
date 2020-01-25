from sqlalchemy import Column, String
from ...data.common import Base
from ...data.common.mixin import Mixin


class User(Mixin, Base):
    first_name = Column(String(200), nullable=True)
    last_name = Column(String(200), nullable=True)
    email = Column(String(320), unique=True)
    picture = Column(String(2048), unique=True)

    def find(self, email):
        users = Mixin.find(self, email=email)
        try:
            return users[0]
        except IndexError as e:
            return None
