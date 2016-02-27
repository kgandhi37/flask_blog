# model of authors use classes

from flask_blog import db

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(80))
    email = db.Column(db.String(35), unique=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(60)) # hashed pass always 60 char, if any more chars could take up more storage in longrun
    is_author = db.Column(db.Boolean)
    
    posts=db.relationship('Post', backref='author', lazy='dynamic') # relating author and posts
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    
    def __init__(self, fullname, email, username, password, is_author=False):  
        self.fullname = fullname
        self.email = email
        self.username = username
        self.password = password
        self.is_author = is_author
        
    def __repr__(self): 
        return '<Author %r>' % self.username 