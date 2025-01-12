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
    
    rating = invoke(f'select SongID, avg(Rating) as rating, count(*) as `count` from Review group by SongID having SongID = {id}').fetchone()
    user_review = invoke(f'select * from Review where SongID = {id} and UserID = {session['userid']}').fetchone() 

    if song is None:
        abort(404)

    liked_users = invoke(f'''select * from User user where exists (
                         select * from LikeSong where UserID = user.UserID and SongID = {id}
                         )''').fetchall()

    return render_template('/song/details.html', song=song, liked_users=liked_users, rating=rating, user_review=user_review)


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