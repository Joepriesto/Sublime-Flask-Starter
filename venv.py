import virtualenv
import os
import pip

class FlaskVitrualEnv(object):
	"""
	Creates a virtualenv for the """
	def __init__(self, path):
		super(FlaskVitrualEnv, self).__init__()
		self.path = path

	def createEnv(self):
		virtualenv.create_environment(self.path)
		execfile(os.path.join(self.path, "bin", "activate_this.py"))

	def installModules(self):
		requirements = os.path.join(os.path.dirname(os.path.realpath(__file__)), "requirements.txt")
		pip.main(["install", "--prefix", venv_dir, "-r", requirements])


