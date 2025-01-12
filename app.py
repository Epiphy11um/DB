from flask import Flask, render_template, redirect, session

from views.auth import auth_bp
from views.concert import concert_bp
from views.album import album_bp
from views.band import band_bp
from views.song import song_bp
from views.review import review_bp

app = Flask(__name__)
app.secret_key = '555555'

@app.route("/")
def index():
    if 'username' not in session:
        return redirect('/login')
    
    return render_template('index.html')

app.register_blueprint(auth_bp)
app.register_blueprint(concert_bp)
app.register_blueprint(album_bp)
app.register_blueprint(band_bp)
app.register_blueprint(song_bp)
app.register_blueprint(review_bp)

if __name__ == '__main__':
    app.run(debug=True)