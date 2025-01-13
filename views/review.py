from flask import render_template, request, redirect, url_for, session, abort, Blueprint
from db import *

review_bp = Blueprint('review', __name__)

@review_bp.route('/review')
def index():
    reviews = invoke(f'''select * from Review
                     inner join Album on Album.AlbumID = Review.AlbumID
                     inner join User on User.UserID = Review.UserID''')
    
    return render_template('review/index.html', reviews=reviews)

@review_bp.route('/album/<int:album_id>/review/<int:user_id>')
def details(album_id: int, user_id: int):
    review = invoke(f'''select * from Review
                    inner join Album on Album.AlbumID = Review.AlbumID
                    inner join User on User.UserID = Review.UserID
                    where Review.AlbumID = {album_id} and Review.UserID = {user_id}''').fetchone()
    
    if review is None:
        abort(404)

    editable = review['UserID'] == session['userid'] or session['usertype'] == 'manager'

    return render_template('/review/details.html', review=review, editable=editable)

@review_bp.route('/album/<int:album_id>/review/')
def list(album_id: int):
    album = invoke(f'select * from Album where AlbumID = {album_id}').fetchone()

    if album is None:
        abort(404)

    reviews = invoke(f'''select * from Review
                       inner join User on Review.UserID = User.UserID
                       where AlbumID = {album_id}''')
    return render_template('/review/list.html', album=album, reviews=reviews)

@review_bp.route('/album/<int:album_id>/review/new', methods=['GET', 'POST'])
def new(album_id: int):
    if request.method == 'GET':
        album = invoke(f'select * from Album where AlbumID = {album_id}')
        return render_template('/review/new.html', album=album)
    
    rating = request.form['rating']
    comment = request.form['comment']

    invoke(f'''insert into Review(AlbumID, UserID, Rating, Comment)
           values ({album_id}, {session['userid']}, {rating}, "{comment}")''')
    
    return redirect(url_for('review.details', album_id=album_id, user_id=session['userid']))
    
@review_bp.route('/album/<int:album_id>/review/edit', methods=['GET', 'POST'])
def edit(album_id: int):
    if request.method == 'GET':
        review = invoke(f'''select * from Review
                          inner join Album on Album.AlbumID = Review.AlbumID
                          where Review.AlbumID = {album_id} and Review.UserID = {session['userid']}''').fetchone()
        
        if review is None:
            return redirect(url_for('review.new', album_id=album_id))
        
        return render_template('review/edit.html', review=review)
    
    rating = request.form['rating']
    comment = request.form['comment']

    invoke(f'''update Review set Rating = {rating}, Comment = "{comment}"
               where AlbumID = {album_id} and UserID = {session['userid']}''')

    return redirect(url_for('review.details', album_id=album_id, user_id=session['userid']))