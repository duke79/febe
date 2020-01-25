import os
import pythoncom
import win32com.client

from core.singleton import Singleton


class NetworkPath(object):
	"""
	Converts local path to network (UNC) path.
	Ref: https://overthere.co.uk/2014/09/02/python-local-path-to-unc/
	"""
	__metaclass__ = Singleton

	def __init__(self):
		super(NetworkPath, self).__init__()
		pythoncom.CoInitialize()
		obj_wmi_service = win32com.client.Dispatch('WbemScripting.SWbemLocator')
		obj_s_wbem_services = obj_wmi_service.ConnectServer('.', 'root\cimv2')
		items = obj_s_wbem_services.ExecQuery('SELECT * FROM Win32_Share')
		self.shares_lookup = {str(share.Path): str(share.Name) for share in items if
							  share.Path and not '$' in share.Name and
							  not share.Name == 'Users'}
		self.shares = sorted((x for x in self.shares_lookup.keys()), key=len, reverse=True)

	def convert(self, local_path):
		if local_path[:2] == '\\\\':
			# Path is already UNC.
			return local_path
		for share_path in self.shares:
			if local_path.lower().startswith(share_path.lower()):
				# We have a match. Return the UNC path.
				if local_path[len(share_path)] == '\\':
					path_end = local_path[len(share_path) + 1:]
				else:
					path_end = local_path[len(share_path):]

				unc_path = os.path.join('\\\\{0:s}'.format(os.getenv('COMPUTERNAME')),
										self.shares_lookup[share_path],
										path_end)
				return unc_path
		# No match found.
		return None
