import sublime
import sublime_plugin
import os

FLASK_CODE = '''from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()'''


class FlaskStarterBase(object):
    @staticmethod
    def createFolder(name, paths):
        if not len(paths):
            raise ValueError("No path data available from SideBar")
        else:
            try:
                path = os.path.join(paths[0], name)
                if not os.path.exists(path):
                    os.makedirs(path)
                return path
            except PermissionError as e:
                raise ValueError(("name = %(1)s & paths = %(2)s" % {"1": name, "2": paths}))


    @staticmethod
    def createSubFiles(name, path):
        dirs = [os.path.join(path, 'static'), os.path.join(path, 'templates')]
        for dir in dirs:
            if not os.path.exists(dir):
                os.makedirs(dir)
        appPath = os.path.join(path, (name + '.py'))
        with open(appPath, 'w') as f:
            f.write(FLASK_CODE)


class RelativeflaskCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        f = self.view.file_name()
        self.path = [self.getFolderName(f)]
        sublime.active_window().show_input_panel(
            "Please enter Project Name:",
            '', lambda s: self.rest(s), None, None)

    def rest(self, name):
        folderName = FlaskStarterBase.createFolder(name, self.path)
        FlaskStarterBase.createSubFiles(name, folderName)

    def getFolderName(self, file):
        return os.path.dirname(file)


class NewflaskCommand(sublime_plugin.WindowCommand):
    def run(self, paths=[]):
        self.path = paths
        self.window.show_input_panel(
            "Please enter Project Name:", '', lambda s: self.doRest(s), None, None)

    def doRest(self, name):
        folderName = FlaskStarterBase.createFolder(name, self.path)
        FlaskStarterBase.createSubFiles(name, folderName)
