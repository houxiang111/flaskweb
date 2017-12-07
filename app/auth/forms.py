# -*- coding: utf-8 -*-
     
from flask.ext.wtf import FlaskForm
from wtforms import StringField ,PasswordField,BooleanField,SubmitField
from wtforms.validators import Required,Length,Email,Regexp,EqualTo,DataRequired
from wtforms import ValidationError
from ..models import User

class LoginForm(FlaskForm):
    email=StringField('注册邮件',validators=[Required(),Length(1,64),Email()])
    password=PasswordField('登入密码',validators=[Required()])
    remember_me=BooleanField('请记住我')
    submit = SubmitField('登入')



class RegisterForm(FlaskForm):                                                                                              
    email = StringField('注册邮箱', validators=[Required(), Length(1,64),Email()])
    username = StringField('用户名', validators=[Required(), Length(1,64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,'用户名不正确')])
    password = PasswordField('登入密码', validators=[Required()])
    password2 = PasswordField('确认密码', validators=[Required(), EqualTo('password', message='密码要一致性哦')])
    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已被注册')
           
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已被注册')


class ResetPasswordForm(FlaskForm):                                                                                              
    email = StringField('用户邮箱', validators=[Required(), Length(1,64),Email()])
    submit = SubmitField('更新密码')


class PasswordForm(FlaskForm):                                                                                              
    password = PasswordField('新密码', validators=[Required()])
    password2 = PasswordField('确认新密码', validators=[Required(), EqualTo('password', message='密码要一致性哦')])
    submit = SubmitField('更新')
