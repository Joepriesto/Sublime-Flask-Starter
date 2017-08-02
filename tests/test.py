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
        testfile = os.path.join(os.path.expanduser("~"),"t.py")
        file = os.open(testfile, os.O_CREAT)
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
            
    def clearProject(self, path):
        rmtree(path)

    def testCreateFolders(self):
        name = 'TestProject'
        startDirectory, filename = os.path.split(self.view.file_name())
        expectedDirectory = os.path.join(startDirectory, name)
        self.assertFalse(os.path.exists("/t.py"), msg="A file exists at root!!!")
        # self.assertIsNot(startDirectory, "/", 
        #     msg=("file_name = %(1)s & cwd = %(2)s, dir = %(4)s & dirname= %(3)s" % {"1": self.view.file_name(), "2": os.getcwd(), "3": startDirectory, "4": os.path.dirname(os.getcwd())}))
        flask_startr.FlaskStarterBase.createFolder(name, [startDirectory])
        self.assertTrue(os.path.exists(expectedDirectory), msg="Project Creation Test Failed")
        self.clearProject(expectedDirectory)

    def testRelativeCommand(self):
        name = 'TestProject'
        startDirectory, filename = os.path.split(self.view.file_name())
        expectedDirectory = os.path.join(startDirectory, name)
        tCommand = flask_startr.RelativeflaskCommand(self.view)
        tCommand.path = [startDirectory]
        tCommand.rest(name)
        self.assertTrue(os.path.exists(expectedDirectory), msg="Project Creation Test Failed")
        self.clearProject(expectedDirectory)

    def testExceptionMessage(self):
        directory = "/"
        name = "Fail"
        with self.assertRaises(ValueError) as cm:
            flask_startr.FlaskStarterBase.createFolder(name, [directory])


if __name__ == '__main__':
    unittest.main()
