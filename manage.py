import os
from FlaskApp import create_app, db
from FlaskApp import models as User
from flask_script import Manager, Shell

app = create_app('default')
manager = Manager(app)

def make_shell_context():
    return dict(app=app, db = db, User = user)

manager.add_command("shell", Shell(make_context = make_shell_context))

if __name__ == '__main__':
    manager.run()
