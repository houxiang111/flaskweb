# -*- coding: utf-8 -*-
    
from app import create_app,db
from app.models import User,Role
from flask.ext.script import Manager,Shell
from flask.ext.migrate import Migrate,MigrateCommand
import os,threading



app = create_app('development')
manager = Manager(app)
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)


def make_shell_context():
    return dict(app = app,db = db,Role=Role,User=User)
manager.add_command("shell",Shell(make_context=make_shell_context))




if __name__ == '__main__':
    manager.run()

