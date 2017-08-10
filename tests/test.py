import unittest
import sublime
import os
import sys
from shutil import rmtree

version = sublime.version()


# for testing internal function
if version < '3000':
    # st2
    flask_startr = sys.modules["flask-starter"]
else:
    # st3
    flask_startr = sys.modules["Sublime-Flask-Starter.flask-starter"]


class FlaskStarterTestCase(unittest.TestCase):

    def setUp(self):
        os.chdir(os.path.expanduser("~"))
        testfile = os.path.join(os.path.expanduser("~"), "t.py")
        testfile = os.path.join(os.path.expanduser("~"),"t.py")
        self.view = sublime.active_window().open_file(testfile)
        self.view.run_command("save")
        s = sublime.load_settings("Preferences.sublime-settings")
        s.set("close_windows_when_empty", False)

    def tearDown(self):
        if self.view:
            self.view.set_scratch(True)
            self.view.window().focus_view(self.view)
            self.view.window().run_command("close_file")
        os.remove("t.py")

    @staticmethod
    def clearProject(path):
        rmtree(path)

    def testCreateFolders(self):
        name = 'TestProject'
        startDirectory = os.path.split(self.view.file_name())[0]
        expectedDirectory = os.path.join(startDirectory, name)
        self.assertFalse(os.path.exists("/t.py"), msg="A file exists at root!!!")
        flask_startr.FlaskStarterBase.createFolder(name, [startDirectory])
        self.assertTrue(os.path.exists(expectedDirectory),
                        msg="Project Creation Test Failed")
        self.clearProject(expectedDirectory)

    def testRelativeCommand(self):
        name = 'TestProject'
        startDirectory = os.path.split(self.view.file_name())[0]
        expectedDirectory = os.path.join(startDirectory, name)
        tCommand = flask_startr.RelativeflaskCommand(self.view)
        tCommand.path = [startDirectory]
        tCommand.rest(name)
        self.assertTrue(os.path.exists(expectedDirectory),
                        msg="Project Creation Test Failed")
        self.clearProject(expectedDirectory)

    def testExceptionMessage(self):
        directory = "/"
        name = "Fail"
        with self.assertRaises(ValueError):
            flask_startr.FlaskStarterBase.createFolder(name, [directory])


if __name__ == '__main__':
    unittest.main()
