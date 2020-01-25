import hashlib

from sqlalchemy import Column, String

from ...data.common import Base
from ...data.common.mixin import Mixin


class JsonWithHash(Mixin, Base):
	"""
	A table to store unstructured data that links to some other table through unique sha
	The UID is supposed to be consistently generatable from the data that this table's row links to.
	"""
	hash_id = Column(String(1033), nullable=False, unique=True)

	def __init__(self, json_data="", data_for_hash=""):
		"""
		:param json_data:
		:param data_for_hash: Hash from this same data should be used while retrieving the row.
		"""
		self.json_data = json_data
		self.hash_id = JsonWithHash.data_to_hash(data_for_hash)

	@staticmethod
	def data_to_hash(data):
		hash_id = hashlib.sha512(data)
		hash_id = hash_id.hexdigest()
		return hash_id
