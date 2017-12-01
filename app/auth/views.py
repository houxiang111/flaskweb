# -*- coding: utf-8 -*-
     
from flask import render_template

@auth.route('/login')
def login():
    return render_template('auth/login.html')
