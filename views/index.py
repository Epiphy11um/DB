from flask import render_template, request, redirect, url_for, session, abort, Blueprint
from db import *
from datetime import datetime

index_bp = Blueprint('index', __name__)

@index_bp.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    
    liked_albums = invoke(f'''select * from Album where exists (
                          select * from LikeAlbum where Album.AlbumID = LikeAlbum.AlbumID and UserID = {session['userid']})''')
    liked_songs = invoke(f'''select * from Song where exists (
                          select * from LikeSong where Song.SongID = LikeSong.SongID and UserID = {session['userid']})''')
    liked_bands = invoke(f'''select * from Band where exists (
                          select * from LikeBand where Band.BandID = LikeBand.BandID and UserID = {session['userid']})''')

    return render_template('index.html', liked_albums=liked_albums, liked_songs=liked_songs, liked_bands=liked_bands)
