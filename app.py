from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///channels.db'
db = SQLAlchemy(app)

class Channel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    youtube_url = db.Column(db.String(200), nullable=False)

@app.route('/')
def index():
    categories = db.session.query(Channel.category).distinct().all()
    channels = Channel.query.all()
    return render_template('index.html', categories=categories, channels=channels)

@app.route('/add', methods=['POST'])
def add_channel():
    name = request.form['name']
    category = request.form['category']
    youtube_url = request.form['youtube_url']
    
    new_channel = Channel(name=name, category=category, youtube_url=youtube_url)
    db.session.add(new_channel)
    db.session.commit()
    
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_channel(id):
    channel = Channel.query.get(id)
    if channel:
        db.session.delete(channel)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
