import os
from app import create_app
from flask.ext.script import Manager, Shell

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)

def make_shell_content():
    return dict(app=app)
manager.add_command("shell", Shell(make_shell_content()))

if __name__ == '__main__':
    manager.run()