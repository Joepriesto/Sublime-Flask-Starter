import sys
import os

try:
    virtualenv = sys.modules["Virtualenv.commands"]
except KeyError:
    print("module not found")


class FlaskVirtualEnv():
    """
    Creates a virtualenv for the """
    def __init__(self, path):
        self.path = path

    def createEnv(self):
        virtualenv.NewVirtualenvCommand().run()
