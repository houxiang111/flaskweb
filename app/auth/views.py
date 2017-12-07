# -*- coding: utf-8 -*-
     
from flask import render_template,redirect,request,url_for,flash
from flask.ext.login import login_user,login_required,logout_user,current_user
from . import auth
from ..models import User
from ..email import send_email
from .forms import LoginForm,RegisterForm,ResetPasswordForm,PasswordForm
from .. import db

@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('用户名或密码不对哦')
    return render_template('auth/login.html',form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已经退出登入')
    return redirect(url_for('main.index'))

@auth.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user=User(email=form.email.data,username=form.username.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        token = user.get_token()
        send_email(user.email,'确认账户','auth/email/confirm',user=user,token=token)
        flash('请查收邮箱哦!!!')
        return  redirect(url_for('main.index'))
    return render_template('auth/register.html',form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('您已经确认账户,谢谢')
    else:
        flash('错误的连接信息或者链接过期')
    return redirect(url_for('main.index'))

@auth.before_app_request
def before_request():
    if current_user.is_authenticated and not current_user.confirmed and request.blueprint !='auth' and request.endpoint!='static':
        return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.confirmed and current_user.is_anonymous:
        return redirect(urL_for('main.index'))
    return render_template('auth/unconfirmed.html')



@auth.route('/confirmed')
@login_required
def resend_confirmation():    
        token = current_user.get_token()
        send_email(current_user.email,'确认账户','auth/email/confirm',user=current_user,token=token)
        flash('请查收邮箱哦!!!')
        return  redirect(url_for('main.index'))


@auth.route('/Reset',methods=['GET','POST'])
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token
            send_email(user.email,'重新设定密码','auth/email/resetpassword',user=user,token=token)
            flash('更改密码的邮箱已发送，请注意查收!!!')
            return redirect(url_for('auth.login'))
        else:
            flash('木有查到邮箱，请确保邮箱准确!!!')
            return redirect(url_for('auth.reset_password'))
    return render_template('auth/reset_password.html',form = form)
 

@auth.route('/Reset/<token>',methods=['GET','POST'])
def passwordreset(token):
    form = PasswordForm()
    if form.validate_on_submit():
        User.resetpassword(token,form.password.data)
        db.session.commit()
        flash('您已更新密码.')
        return redirect(url_for('auth.login'))
    return render_template('auth/passwordreset.html', form=form)   
