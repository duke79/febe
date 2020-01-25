import os


class Environment:
	scm_dir = "SCM_DIR"
	mkmk_build_args = "MKMK_BUILD_ARGS"
	flask_as_json = "FLASK_AS_JSON"
	auto_import_temp_dir = "AUTO_IMPORT_TEMP_DIR"

	def getScriptPath(self):
		return os.path.realpath(__file__)

	def getScriptDirPath(self):
		return os.path.dirname(self.getScriptPath())

	def getParentDirPath(self, path):
		return os.path.dirname(path)

	def getEnvironmentVariable(self, key):
		return os.environ.get(key)

	def setEnvironmentVariable(self, key, value):
		os.environ[key] = value

	def getPath(self):
		return self.getEnvironmentVariable("path")

	def setPath(self, path):
		self.setEnvironmentVariable("path", path)

	def appendToPath(self, path):
		self.setPath(self.getPath() + ";" + path)


class EnvCounter:
	def __init__(self, key):
		self.key = str(key) + "_counter"
		self.value = 0

		try:
			counter = os.environ[self.key]
			self.value = counter
		except Exception as e:
			os.environ[self.key] = "0"

	def increment(self):
		counter = os.environ[self.key]
		self.value = int(counter) + 1
		os.environ[self.key] = str(self.value)
		return self
