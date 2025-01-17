from flask import Flask, render_template, request, redirect, url_for, session, abort, Blueprint
from db import *

song_bp = Blueprint('song', __name__)

@song_bp.route('/song/')
def index():
    songs = invoke(f'''
                   select 
                   exists (
                       select * from LikeSong where UserID = {session['userid']} and SongID = Song.SongID
                   ) as liked,
                   Song.*, Album.* from Song
                   inner join Album on Song.AlbumID = Album.AlbumID''').fetchall()
    return render_template('song/index.html', songs=songs)

@song_bp.route('/song/<int:id>')
def details(id: int):
    song = invoke(f'''select * from Song
                      inner join Album on Song.AlbumID = Album.AlbumID
                      where SongID = {id}''').fetchone()
    
    if song is None:
        abort(404)

    liked_users = invoke(f'''select * from User user where exists (
                         select * from LikeSong where UserID = user.UserID and SongID = {id}
                         )''').fetchall()
    
    rel = invoke(f'select * from _UserToBand where UserID = {session['userid']} and BandID = {song['BandID']}').fetchone()

    editable = rel is not None or session['usertype'] == 'manager'

    return render_template('/song/details.html', song=song, liked_users=liked_users, editable=editable)

@song_bp.route('/song/<int:id>/edit', methods=['GET', 'POST'])
def edit(id: int):
    if request.method == 'GET':
        song = invoke(f'select * from Song where SongID = {id}').fetchone()
        return render_template('/song/edit.html', song=song)
    
    name = request.form['name']
    oa = request.form['originalAuthor']
    genre = request.form['genre']

    invoke(f'update Song set SongName = "{name}", OriginalAuthor = "{oa}", Genre = "{genre}" where SongID = {id}')
    return redirect(url_for('song.details', id=id))

@song_bp.route('/song/<int:id>/like', methods=['POST'])
def like(id: int):
    userid = session['userid']

    rel = invoke(f'select * from LikeSong where UserID = {userid} and SongID = {id}').fetchone()

    if rel is None:
        invoke(f'insert into LikeSong values ({userid}, {id})')
        return { 'liked': True }
    else:
        invoke(f'delete from LikeSong where UserID = {userid} and SongID = {id}')
        return { 'liked': False }
    
@song_bp.route('/song/<int:id>/delete', methods=['POST'])
def delete(id: int):
    if 'userid' not in session:
        abort(403)

    song = invoke(f'select * from Song inner join Album on Album.AlbumID = Song.AlbumID where SongID = {id}').fetchone()

    if song is None:
        abort(404)

    rel = invoke(f'select * from _UserToBand where BandID = {song['BandID']} and UserID = {session['userid']}').fetchone()

    if rel is None:
        abort(403)

    pos = song['Order']
    invoke(f'update Song set `Order` = `Order` - 1 where `Order` > {pos}')
    invoke(f'delete from Song where SongID = {id}')

    return redirect(url_for('album.details', id=song['AlbumID']))