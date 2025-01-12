from flask import Flask, render_template, request, redirect, url_for, session, abort, Blueprint
from db import *

concert_bp = Blueprint('concert', __name__)

@concert_bp.route('/concert/')
def index():
    concerts = invoke('select * from Concert inner join Band on Concert.BandID = Band.BandID;').fetchall()
    return render_template('/concert/index.html', concerts=concerts)

@concert_bp.route('/concert/new', methods=['GET', 'POST'])
def new():
    if request.method == 'GET':
        userid = session['userid']
        bands = invoke(f'''select * from Band b where exists (
                       select * from _UserToBand where UserID = {userid} and BandID = b.BandID
                       )''')
        return render_template('/concert/new.html', bands=bands)
    
    name = request.form['name']
    location = request.form['location']
    date = request.form['date']
    band_id = request.form['band_id']

    concert_id = invoke_insertion(f'''insert into Concert(ConcertName, Location, ConcertDate, BandID)
                                  VALUES ("{name}", "{location}", "{date}", {band_id})''')
    
    return redirect(url_for('concert.details', id=concert_id))
    
    
@concert_bp.route('/concert/<int:id>')
def details(id: int):
    concert = invoke(f'select * from Concert where ConcertID = {id}').fetchone()

    if concert is None:
        abort(404)

    band = invoke(f'select * from Band where BandID = {concert['BandID']}').fetchone()
    rel = invoke(f'select * from _UserToBand where BandID = {concert['BandID']} and UserID = {session['userid']}').fetchone()
    editable = (rel is not None)

    return render_template('/concert/details.html', concert=concert, band=band, editable=editable)

@concert_bp.route('/concert/<int:id>/edit', methods=['GET', 'POST'])
def edit(id: int):
    if request.method == 'GET':
        userid = session['userid']

        concert = invoke(f'select * from Concert where ConcertID = {id}').fetchone()

        if concert is None:
            abort(404)

        bands = invoke(f'''select * from Band b where exists (
                       select * from _UserToBand where UserID = {userid} and BandID = b.BandID
                       )''')

        return render_template('/concert/edit.html', concert=concert, bands=bands)
    
    name = request.form['name']
    location = request.form['location']
    date = request.form['date']
    band_id = request.form['band_id']

    invoke(f'update Concert set ConcertName="{name}", Location="{location}", ConcertDate="{date}", BandID={band_id} where ConcertID={id}')

    return redirect(url_for('concert.details', id=id))

@concert_bp.route('/concert/<int:id>/delete')
def delete(id: int):
    userid = session['userid']
    concert = invoke(f'select * from Concert where ConcertID = {id}').fetchone()

    rel = invoke(f'select * from _UserToBand where BandID = {concert['BandID']} and UserID = {userid}').fetchone()

    if rel is None:
        abort(403)

    invoke(f'delete from Concert where ConcertID = {id}')

    return redirect(url_for('concert.index'))
