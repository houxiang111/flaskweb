# -*- coding: utf-8 -*-
    
from flask import Flask,render_template,redirect,url_for,session,flash
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.wtf import Form
from flask.ext.sqlalchemy import SQLAlchemy
from wtforms import StringField,SubmitField
from wtforms.validators import Required
from datetime import datetime
from flask.ext.script import Shell
from flask.ext.migrate import Migrate,MigrateCommand

class nameform(Form):
    name = StringField('name',validators=[Required()])
    submit = SubmitField('submit')


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:19930119@127.0.0.1:3306/flask'
app.config['SQLALCHEMY_COMMIT_IN_TEARDOWN'] = True
app.config['SECRET_KEY'] = 'hard to guess string'
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    users = db.relationship('User',backref='role')
    def __repr__(self):
        return '<Role %r>' %self.name
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    def __repr__(self):
        return '<User %r>' %self.username

def make_shell_context():
    return dict(app = app,db = db,Role=Role,User=User)
manager.add_command("shell",Shell(make_context=make_shell_context))

@app.route('/',methods=['GET','POST'])
def index():
    name = None
    form = nameform()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known']=False
            db.session.commit()
        else:
            session['known']=True
        session['name'] = form.name.data
        form.name.data=''
        return redirect(url_for('index'))
    return render_template('index.html',form=form,name=session.get('name'),known=session.get('known',False),current_time=datetime.utcnow())


@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name = name)

@app.errorhandler(404)
def PagerNotFound(e):
    return render_template("404.html"),404

@app.errorhandler(500)
def ServerError(e):
    return render_template("500.html"),500

if __name__ == '__main__':
    manager.run()

