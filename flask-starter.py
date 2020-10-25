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

FLASK_FACTORY_CODE = '''
import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
'''


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
            except PermissionError:
                raise ValueError(("name = %(1)s & paths = %(2)s" % {"1": name, "2": paths}))


    @staticmethod
    def createSubFiles(name, path, type="basic"):
        dirs = [os.path.join(path, 'static'), os.path.join(path, 'templates')]
        for d in dirs:
            if not os.path.exists(d):
                os.makedirs(d)
        appPath = os.path.join(path, (name + '.py'))
        with open(appPath, 'w') as f:
            f.write(FLASK_CODE) if type == "basic" else f.write(FLASK_FACTORY_CODE) if type == "factory" else f.write("App type not found.")


class RelativeflaskCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        f = self.view.file_name()
        self.path = [self.getFolderName(f)]
        sublime.active_window().show_input_panel(
            "Please enter Project Name:",
            '', self.rest, None, None)

    def rest(self, name):
        folderName = FlaskStarterBase.createFolder(name, self.path)
        FlaskStarterBase.createSubFiles(name, folderName)

    @staticmethod
    def getFolderName(file):
        return os.path.dirname(file)

class RelativeflaskFactoryCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        f = self.view.file_name()
        self.path = [self.getFolderName(f)]
        sublime.active_window().show_input_panel(
            "Please enter Project Name:",
            '', self.rest, None, None)

    def rest(self, name):
        folderName = FlaskStarterBase.createFolder(name, self.path)
        FlaskStarterBase.createSubFiles(name, folderName, "factory")

    @staticmethod
    def getFolderName(file):
        return os.path.dirname(file)

class NewflaskCommand(sublime_plugin.WindowCommand):
    def run(self, paths=None):
        self.path = paths or []
        self.window.show_input_panel(
            "Please enter Project Name:", '', self.doRest, None, None)

    def doRest(self, name):
        folderName = FlaskStarterBase.createFolder(name, self.path)
        FlaskStarterBase.createSubFiles(name, folderName)

class NewflaskFactoryCommand(sublime_plugin.WindowCommand):
    def run(self, paths=None):
        self.path = paths or []
        self.window.show_input_panel(
            "Please enter Project Name:", '', self.doRest, None, None)

    def doRest(self, name):
        folderName = FlaskStarterBase.createFolder(name, self.path)
        FlaskStarterBase.createSubFiles(name, folderName, "factory")