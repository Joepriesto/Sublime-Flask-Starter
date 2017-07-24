import unittest
import sublime
import os

version = sublime.version()


class FlaskStarterTestCase(unittest.TestCase):

    def setUp(self):
        file = open("t.py", mode="w")
        file.close()
        self.view = sublime.active_window().open_file("t.py")
        s = sublime.load_settings("Preferences.sublime-settings")
        s.set("close_windows_when_empty", False)

    def tearDown(self):
        if self.view:
            self.view.set_scratch(True)
            self.view.window().focus_view(self.view)
            self.view.window().run_command("close_file")

    def testCommand(self):
        print(self.view.file_name())
        self.view.run_command("relativeFlask", {'s': "TestProject"})
        self.assertTrue(os.path.exists(os.path.join(self.view.file_name(),
                                                    'TestProject'),
                        msg="Project Creation Test Failed"))
