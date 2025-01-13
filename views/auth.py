from flask import Flask, render_template, request, redirect, url_for, session, abort, Blueprint
from db import *
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/auth/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))

@auth_bp.route("/auth/login", methods=['GET', 'POST'])  # 登录
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')
    
    name = request.form.get("username")
    pwd = request.form.get("password")
    ans = invoke(f"select * from User where UserName = '{name}'")
    user = ans.fetchone()
    if user is None or user['Password'] != pwd:
        return render_template('auth/login.html', error="登录凭据无效")

    session.update({
        'userid': user['UserID'],
        'username': name,
        'usertype': user['Type'],
    })

    print(user)
    return redirect('/')


@auth_bp.route("/auth/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("auth/register.html")

    name = request.form.get("username")
    pwd = request.form.get("password")
    pwd2 = request.form.get("password2")
    type = request.form.get("userType")
    user = invoke(f"select * from User where UserName = '{name}'").fetchone()
    print(user)

    if pwd2 != pwd:
        return render_template('/auth/register.html', error="密码不一致")
    
    if user is not None:
        return render_template('/auth/register.html', error="该用户名已经存在")
    
    if type == '':
        return render_template('/auth/register.html', error="请选择用户类型")
    
    invoke(f"INSERT INTO User(UserName, Password, Type) VALUES ('{name}', '{pwd}', '{type}')")
    return redirect(url_for('auth.login'))
