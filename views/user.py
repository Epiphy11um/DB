from flask import Flask, render_template, request, redirect, url_for, session, abort, Blueprint
from db import *

user_bp = Blueprint('user', __name__)

@user_bp.route('/user/<int:id>')
def details(id: int):
    user = invoke(f'select * from User where UserID = {id}').fetchone()

    if user is None:
        abort(404)

    return render_template('/user/details.html', user=user)


@user_bp.route('/user/edit', methods=['GET', 'POST'])
def edit():
    if 'userid' not in session:
        abort(404)

    if request.method == 'GET':
        user = invoke(f'select * from User where UserId = {session['userid']}').fetchone()
        return render_template('/user/edit.html', user=user)
    
    realname = request.form['real_name']
    age = request.form['age']
    job = request.form['job']
    edu = request.form['edu']

    invoke(f'''update User set RealName="{realname}", Age={age}, Job="{job}", EducationLevel="{edu}"
           where UserID = {session['userid']}''')
    return redirect(url_for('user.details', id=session['userid']))


