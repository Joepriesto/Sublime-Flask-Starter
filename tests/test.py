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
        file = os.open("t.py", os.O_CREAT)
        self.view = sublime.active_window().open_file("t.py")
        self.view.run_command("save")
        s = sublime.load_settings("Preferences.sublime-settings")
        s.set("close_windows_when_empty", False)

    def tearDown(self):
        if self.view:
            self.view.set_scratch(True)
            self.view.window().focus_view(self.view)
            self.view.window().run_command("close_file")
        os.remove("t.py")
            
    def clearProject(self, path):
        rmtree(path)

    def testCreateFolders(self):
        name = 'TestProject'
        startDirectory = os.path.dirname(self.view.file_name())
        expectedDirectory = os.path.join(startDirectory, name)
        flask_startr.FlaskStarterBase.createFolder(name, [startDirectory])
        self.assertTrue(os.path.exists(expectedDirectory), msg="Project Creation Test Failed")
        self.clearProject(expectedDirectory)

    def testRelativeCommand(self):
        name = 'TestProject'
        startDirectory = os.path.dirname(self.view.file_name())
        expectedDirectory = os.path.join(startDirectory, name)
        tCommand = flask_startr.RelativeflaskCommand(self.view)
        tCommand.path = [startDirectory]
        tCommand.rest(name)
        self.assertTrue(os.path.exists(expectedDirectory), msg="Project Creation Test Failed")
        self.clearProject(expectedDirectory)



if __name__ == '__main__':
    unittest.main()
