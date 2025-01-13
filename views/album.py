from flask import Flask, render_template, request, redirect, url_for, session, abort, Blueprint
from db import *
from datetime import datetime

album_bp = Blueprint('album', __name__)


@album_bp.route('/album/')
def index():
    albums = invoke(f'''
                    select (
                        select count(*) from Song where Song.AlbumID = Album.AlbumID
                    ) as count, 
                    exists (
                        select * from LikeAlbum where UserID = {session['userid']} and AlbumID = Album.AlbumID
                    ) as liked,
                    Album.*, Band.* from Album
                    inner join Band on Album.BandID = Band.BandID''').fetchall()

    return render_template('/album/index.html', albums=albums)


@album_bp.route('/album/new', methods=['GET', 'POST'])
def new():
    if request.method == 'GET':
        userid = session['userid']
        bands = invoke(f'''select * from Band b where exists (
                       select * from _UserToBand where UserID = {userid} and BandID = b.BandID
                       )''')
        return render_template('/album/new.html', bands=bands)
    
    if not request.is_json:
        abort(400)

    data = request.json
    name = data['name']
    desc = data['desc']
    band_id = data['bandId']
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    album_id = invoke_insertion(f'''insert into Album(AlbumName, AlbumDescription, ReleaseDate, BandID)
                                    values ("{name}", "{desc}", "{date}", {band_id})''')
    
    for i, item in enumerate(data['songs']):
        name = item['name']
        genre = item['genre']
        author = item['originalAuthor']
        invoke_insertion(f'''insert into Song(SongName, OriginalAuthor, Genre, AlbumID, `Order`)
                             values ("{name}", "{author}", "{genre}", {album_id}, {i + 1})''')
        
    return redirect(url_for('album.details', id=album_id))

@album_bp.route('/album/<int:id>')
def details(id: int):
    album = invoke(f'select * from Album where AlbumID = {id}').fetchone()

    if album is None:
        abort(404)

    songs = invoke(f'select * from Song where AlbumID = {id} order by `Order` asc')
    liked_users = invoke(f'''select * from User user where exists (
                         select * from LikeAlbum where UserID = user.UserID and AlbumID = {id}
                         )''').fetchall()
    rel = invoke(f'select * from _UserToBand where BandID = {album['BandID']} and UserID = {session['userid']}').fetchone()
    
    editable = rel is not None

    return render_template('/album/details.html', album=album, songs=songs, liked_users=liked_users, editable=editable)

@album_bp.route('/album/<int:id>/like', methods=['POST'])
def like(id: int):
    userid = session['userid']

    rel = invoke(f'select * from LikeAlbum where UserID = {userid} and AlbumID = {id}').fetchone()

    if rel is None:
        invoke(f'insert into LikeAlbum values ({userid}, {id})')
        return { 'liked': True }
    else:
        invoke(f'delete from LikeAlbum where UserID = {userid} and AlbumID = {id}')
        return { 'liked': False }
    
@album_bp.route('/album/<int:id>/add', methods=['GET', 'POST'])
def add(id: int):
    if request.method == 'GET':
        album = invoke(f'select * from Album where AlbumID = {id}')
        songs = invoke(f'select * from Song where AlbumID = {id} order by `Order` asc').fetchall()
        return render_template('/album/add.html', album=album, songs=songs)
    
    pos = request.form['pos']
    name = request.form['name']
    oa = request.form['originalAuthor']
    genre = request.form['genre']

    invoke(f'update Song set `Order` = `Order` + 1 where AlbumID = {id} and `Order` > {pos}')
    invoke(f'''insert into Song(SongName, OriginalAuthor, Genre, AlbumID, `Order`)
           values ("{name}", "{oa}", "{genre}", {id}, {pos + 1})''')
    
    return redirect(url_for('album.details', id=id))
