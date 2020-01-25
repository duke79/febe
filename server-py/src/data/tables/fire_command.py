from sqlalchemy import Column, String, Text
from ...data.common import Base
from ...data.common.mixin import Mixin


class FireCommand(Mixin, Base):
    cmd = Column(Text, nullable=True)
    source = Column(String(200), nullable=True)

    def __init__(self):
        pass

    def insert_cmd(self, cmd, source):
        self.cmd = cmd
        self.source = source
        self.save()
