from flask import Flask, render_template, request, redirect, url_for, session, abort, Blueprint
from db import *
from datetime import datetime

band_bp = Blueprint('band', __name__)


@band_bp.route("/band/")
def index():
    bands = invoke(f'''
                   select 
                   exists (
                       select * from LikeBand where UserID = {session['userid']} and BandID = b.BandID
                   ) as liked,
                   b.* from Band b;''').fetchall()
    print(bands)
    return render_template("/band/index.html", bands=bands)

@band_bp.route("/band/new", methods=['GET', 'POST'])
def new():
    if request.method == 'GET':
        return render_template('band/new.html')
    
    userid = session['userid']
    name = request.form.get('name')
    desc = request.form.get('description')
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    band_id = invoke_insertion(f'insert into Band(BandName, BandDescription, FormationDate) values ("{name}", "{desc}", "{date}");')
    invoke(f'insert into _UserToBand(UserID, BandID, Role) values("{userid}", "{band_id}", "creator")')
    return redirect(url_for('band.details', id=band_id))

@band_bp.route('/band/<int:id>/')
def details(id: int):
    band = invoke(f'select * from Band where BandId = {id}').fetchone()
    if band is None:
        abort(404)

    members = invoke(f'''select * from User user where exists (
                     select * from _UserToBand where UserID = user.UserID and BandID = {id}
                     )''').fetchall()
    concerts = invoke(f'select * from Concert where BandID = {id}').fetchall()
    rel = invoke(f'select Role from _UserToBand where UserID = {session['userid']} and BandID = {id}').fetchone()
    liked_count = invoke(f'select count(*) as `count` from LikeBand where BandID = {id}').fetchone()
    if liked_count is None:
        liked_count = { 'count': 0 }
    editable = (rel is not None)

    return render_template('/band/details.html', band=band, members=members, concerts=concerts, liked_count=liked_count, editable=editable)

@band_bp.route('/band/<int:id>/like', methods=['POST'])
def like(id: int):
    userid = session['userid']

    rel = invoke(f'select * from LikeBand where UserID = {userid} and BandID = {id}').fetchone()

    if rel is None:
        invoke(f'insert into LikeBand values ({userid}, {id})')
        return { 'liked': True }
    else:
        invoke(f'delete from LikeBand where UserID = {userid} and BandID = {id}')
        return { 'liked': False }


@band_bp.route('/band/<int:id>/edit', methods=['GET', 'POST'])
def edit(id: int):
    if request.method == 'GET':
        band = invoke(f'select * from Band where BandId = {id}').fetchone()
        if band is None:
            abort(404)

        return render_template('/band/edit.html', band=band)
    
    name = request.form.get('name')
    desc = request.form.get('description')

    invoke(f'update Band set BandName="{name}", BandDescription="{desc}" where BandID={id}')
    return redirect(url_for('band.details', id=id))