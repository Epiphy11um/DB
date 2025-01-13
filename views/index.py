from flask import render_template, request, redirect, url_for, session, abort, Blueprint
from db import *
from datetime import datetime

index_bp = Blueprint('index', __name__)

@index_bp.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    
    liked_albums = invoke(f'''select (
                            select count(*) from Song where Song.AlbumID = Album.AlbumID 
                          ) as `count`, Album.*, Band.* from Album 
                          inner join Band on Album.BandID = Band.BandID
                          where exists (
                            select * from LikeAlbum where Album.AlbumID = LikeAlbum.AlbumID and UserID = {session['userid']}
                          )''')
    liked_songs = invoke(f'''select * from Song
                         inner join Album on Album.AlbumID = Song.AlbumID
                         where exists (
                          select * from LikeSong where Song.SongID = LikeSong.SongID and UserID = {session['userid']})''')
    liked_bands = invoke(f'''select * from Band
                          where exists (
                          select * from LikeBand where Band.BandID = LikeBand.BandID and UserID = {session['userid']})''')
    part = invoke(f'''select * from Concert
                  inner join Participation on Participation.ConcertID = Concert.ConcertID
                  inner join Band on Concert.BandID = Band.BandID
                  where UserID = {session['userid']}''')
    top_albums = invoke(f'''select
                        (select avg(Rating) from Review where Review.AlbumID = Album.AlbumID) as avg_rating,
                        (select count(*) from Song where Song.AlbumID = Album.AlbumID) as `count`,
                        Album.*, Band.* from Album
                        inner join Band on Album.BandID = Band.BandID
                        order by avg_rating desc
                        limit 8''')
    return render_template('index.html', liked_albums=liked_albums, liked_songs=liked_songs, liked_bands=liked_bands, participation=part, top_albums=top_albums)
