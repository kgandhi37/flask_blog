from flask_blog import db, uploaded_images
from datetime import datetime

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    admin = db.Column(db.Integer, db.ForeignKey('author.id')) # links to author, specific admin of the blog
    posts = db.relationship('Post', backref='blog', lazy='dynamic') 
    
    def __init__(self, name, admin):
        self.name = name
        self.admin = admin
        
    def __repr__(self):
        return '<Blog %r>' % self.name
        
class Post(db.Model): # blog posts within created blog
    id = db.Column(db.Integer, primary_key=True)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    image = db.Column(db.String(255))
    slug = db.Column(db.String(256), unique=True)  # url identifier
    publish_date = db.Column(db.DateTime)
    live = db.Column(db.Boolean)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    
    category=db.relationship('Category', backref=db.backref('posts', lazy='dynamic')) # written this way because 2 way - many to many
    comments = db.relationship('Comment', backref='posts', lazy='dynamic')

    @property 
    def imgsrc(self):
        return uploaded_images.url(self.image)
    
    
    def __init__(self, blog, author, title, body, category, image=None, slug=None, publish_date=None, live=True):
        self.blog_id = blog.id # blog and author passed as object.
        self.author_id = author.id
        self.title = title
        self.body = body
        self.category_id = category.id
        self.image=image
        self.slug = slug
        if publish_date is None:
            self.publish_date = datetime.utcnow() # import datetime - always use utc
        else:
            self.publish_date = publish_date
        self.live = live
        
        
    def __repr__(self):
        return '<Blog Title %r>' % self.title

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment_body = db.Column(db.Text)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    comment_author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    comment_date = db.Column(db.DateTime)
    live = db.Column(db.Boolean)

    def __init__(self, comment_body, post, author, comment_date=None, live=True):
        self.comment_body = comment_body
        self.post_id = post
        self.comment_author_id = author
        if comment_date is None:
            self.comment_date = datetime.utcnow()
        else:
            self.comment_date = comment_date
        self.live = live

    def __repr__(self):
        return '<Comment %r>' % self.id

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        # return '<Category %r>' % self.name - figure out other method, below is one way (for QuerySelectForm)
        return self.name