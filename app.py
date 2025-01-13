from flask import Flask, render_template, redirect, session

from views.index import index_bp
from views.auth import auth_bp
from views.user import user_bp
from views.concert import concert_bp
from views.album import album_bp
from views.band import band_bp
from views.song import song_bp
from views.review import review_bp

app = Flask(__name__)
app.secret_key = '555555'

app.register_blueprint(index_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(concert_bp)
app.register_blueprint(album_bp)
app.register_blueprint(band_bp)
app.register_blueprint(song_bp)
app.register_blueprint(review_bp)

if __name__ == '__main__':
    app.run(debug=True)