# -*- coding: utf-8 -*-
from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask.ext.login import UserMixin
from . import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<Role %r>' % self.name

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    email=db.Column(db.String(64),unique=True,index=True)
    confirmed=db.Column(db.Boolean,default=False)


    def get_token(self,expriation=3000):
        s = Serializer(current_app.config['SECRET_KEY'],expriation)
        token = s.dumps({'confirm':self.id})
        return token

    def confirm(self,token):
        s=Serializer(current_app.config['SECRET_KEY'])
        try:
            data=s.loads(token)
        except:
            return False
        if data.get('confirm') !=self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

    @property
    def password(self):
        raise AttributeError('password in not readable')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)
    
    def __repr__(self):
        return '<User %r>' % self.username
   

    def generate_reset_token(self, expiration=3000):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    @staticmethod
    def resetpassword(token,password):
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = User.query.get(data.get['reset'])
        if user is None:
            return False
        User.password = password
        db.session.add(User)
        return True

@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(int(user_id))
