from flask import render_template, request, redirect, url_for, session, abort, Blueprint
from db import *

review_bp = Blueprint('review', __name__)

@review_bp.route('/review')
def index():
    reviews = invoke(f'''select * from Review
                     inner join Song on Song.SongID = Review.SongID
                     inner join User on User.UserID = Review.UserID''')
    
    return render_template('review/index.html', reviews=reviews)

@review_bp.route('/song/<int:song_id>/review/<int:user_id>')
def details(song_id: int, user_id: int):
    review = invoke(f'''select * from Review
                    inner join Song on Song.SongID = Review.SongID
                    inner join User on User.UserID = Review.UserID
                    where Review.SongID = {song_id} and Review.UserID = {user_id}''').fetchone()
    
    if review is None:
        abort(404)

    editable = review['UserID'] == session['userid'] or session['usertype'] == 'manager'

    return render_template('/review/details.html', review=review, editable=editable)

@review_bp.route('/song/<int:song_id>/review/')
def list(song_id: int):
    song = invoke(f'select * from Song where SongID = {song_id}').fetchone()

    if song is None:
        abort(404)

    reviews = invoke(f'''select * from Review
                       inner join User on Review.UserID = User.UserID
                       where SongID = {song_id}''')
    return render_template('/review/list.html', song=song, reviews=reviews)

@review_bp.route('/song/<int:song_id>/review/new', methods=['GET', 'POST'])
def new(song_id: int):
    if request.method == 'GET':
        song = invoke(f'select * from Song where SongID = {song_id}')
        return render_template('/review/new.html', song=song)
    
    rating = request.form['rating']
    comment = request.form['comment']

    invoke(f'''insert into Review(SongID, UserID, Rating, Comment)
           values ({song_id}, {session['userid']}, {rating}, "{comment}")''')
    
    return redirect(url_for('review.details', song_id=song_id, user_id=session['userid']))
    
@review_bp.route('/song/<int:song_id>/review/edit', methods=['GET', 'POST'])
def edit(song_id: int):
    if request.method == 'GET':
        review = invoke(f'''select * from Review
                          inner join Song on Song.SongID = Review.SongID
                          where Review.SongID = {song_id} and Review.UserID = {session['userid']}''').fetchone()
        
        if review is None:
            return redirect(url_for('review.new', song_id=song_id))
        
        return render_template('review/edit.html', review=review)
    
    rating = request.form['rating']
    comment = request.form['comment']

    invoke(f'''update Review set Rating = {rating}, Comment = "{comment}"
               where SongID = {song_id} and UserID = {session['userid']}''')

    return redirect(url_for('review.details', song_id=song_id, user_id=session['userid']))