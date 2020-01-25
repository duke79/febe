from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.exc import IntegrityError

from ...data.common import Base
from ...data.common.mixin import Mixin
from ...data.tables.user import User


class OAuthIdentity(Mixin, Base):
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    platform_id = Column(String(100), nullable=True)
    # access_token = Column(String(256), nullable=True) # http://bit.ly/2nRfP1R
    # last_active? = Column(DateTime, nullable=False, server_default=func.now())
    platform = Column(String(50), nullable=True)

    __table_args__ = (
        UniqueConstraint('platform_id', 'platform', name='unique_platform_user'),
    )

    def find(self, platform_id, platform):
        # identities = self.session().query(self.user_id)
        # identities = identities.filter(self.platform_id == platform_id and self.platform == platform)
        # identity = identities.first()
        # return identity
        identities = Mixin.find(self, platform_id=platform_id, platform=platform)
        try:
            return identities[0]
        except IndexError as e:
            return None
