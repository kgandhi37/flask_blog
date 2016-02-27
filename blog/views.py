from flask_blog import app 
from flask import render_template, redirect, flash, url_for, session, abort, request 
from blog.form import SetupForm, PostForm, CommentForm
from flask_blog import db, uploaded_images 
from author.models import Author # importing author model
from blog.models import Blog, Post, Category, Comment 
from author.decorators import login_required, author_required
import bcrypt # for secure passwords
from slugify import slugify

# for pagination
POSTS_PER_PAGE = 4

@app.route('/')
@app.route('/index')
@app.route('/index/<int:page>') # for pagination
def index(page=1): # page called and auto set to 1 otherwise other number
    blog = Blog.query.first()
    if not blog:
        return redirect(url_for('setup'))
    posts = Post.query.filter_by(live=True).order_by(Post.publish_date.desc()).paginate(page, POSTS_PER_PAGE, False) 
    # get all posts ordered by date, paginate, False at the end will stop 404 error occuring when checking
    # for further posts. returns a list. check template on how to handle. pagination is not iterable
    # in the template instead of for post in posts we have to use for post in posts.items as its a list
    return render_template('blog/index.html', posts=posts, blog=blog)
    
@app.route('/admin')
@app.route('/admin/<int:page>')
@login_required # decorator check if logged in
@author_required
def admin(page=1):
    if session.get('is_author'):
        posts = Post.query.order_by(Post.publish_date.desc()).paginate(page, POSTS_PER_PAGE, False) 
        return render_template('blog/admin.html', posts=posts)
    else:
        abort(403)
    
@app.route('/setup', methods=('GET', 'POST')) 
def setup():
    form = SetupForm()
    error = ""
    if form.validate_on_submit():
        # securing passwords using bcrypt
        # generate a salt
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(form.password.data, salt)
        # above storing the hashed pass using the bcrypt function hashpw encoded with the salt. always generates a 60char string
        author = Author(
            form.fullname.data, # calling data from the forms
            form.email.data,
            form.username.data,
            hashed_password, # store hashed password
            True # is_author
            )
        db.session.add(author)
        db.session.flush() 
        if author.id:
            blog = Blog(
                form.name.data,
                author.id
                )
            db.session.add(blog)
            db.session.flush()
        else:
            db.session.rollback() # undo operations and go back if error
            error = "Error creating user"
        if author.id and blog.id:
            db.session.commit()
            flash("Blog Created")
            return redirect(url_for('index'))
        else:
            db.session.rollback()
            error = "Error creating blog"
    return render_template('blog/setup.html', form=form, error=error) # form as context, sending error back
    
    
# generate new posts
@app.route('/post', methods=('GET','POST'))
@login_required
@author_required
def post():
    form = PostForm()
    comment_form = CommentForm()
    error=None
    if form.validate_on_submit():
        image = request.files.get('image')
        filename = None
        try:
            filename=uploaded_images.save(image)
        except:
            flash('The image was not uploaded')
        if form.new_category.data:
            new_category = Category(form.new_category.data)
            db.session.add(new_category)
            db.session.flush() # trick again, hasn't committed but creates object, commit in the end.
            category = new_category
        elif form.category.data:
            category_id = form.category.get_pk(form.category.data) # gets primary key (id) of the selection
            category = Category.query.filter_by(id=category_id).first()
        else:
            category=None
        blog = Blog.query.first() # assuming one blog, if system with more than 1 blog - figure out here
        author = Author.query.filter_by(username=session['username']).first()
        title = form.title.data
        body = form.body.data
        slug = slugify(title)
        post = Post(blog, author, title, body, category, filename, slug)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('article', slug=slug)) # sending to article page with slug
        
    return render_template('blog/post.html', form=form, comment_form=comment_form, action="new")

    
    

# rendering article
@app.route('/article/<slug>', methods=('GET','POST')) # article by slug, pass through function below.
def article(slug):
    form = CommentForm()
    post = Post.query.filter_by(slug=slug).first_or_404() # either find the post or return 404
    comments = Comment.query.filter_by(post_id=post.id, live=True).order_by(Comment.comment_date.desc())
    # check if comments exist
    comment_check = Comment.query.first()
    if not comment_check:
        is_comment = 0
    else:
        is_comment = 1

    # posting a comment

    error = None
    if form.validate_on_submit():
        author = Author.query.filter_by(username=session['username']).first()
        comment_body = form.comment_body.data
        comment = Comment(comment_body, post.id, author.id)
        db.session.add(comment)
        db.session.commit()
        flash("Comment posted!")
    return render_template('blog/article.html', post=post, comments=comments, form=form, is_comment=is_comment) 
    
@app.route('/edit/<int:post_id>', methods=('GET','POST'))
@author_required
def edit(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    form = PostForm(obj=post) # assign values to form from object above, inbuilt feature
    if form.validate_on_submit():
        original_image = post.image
        form.populate_obj(post) # loads and replaces post object with contents of the form
        if form.image.has_file():
            image = request.files.get('image')
            try:
                filename = uploaded_images.save(image)
            except:
                flash("Image not uploaded")
            if filename:
                post.image = filename
        else:
            post.image = original_image # post.image has been populated by the form content so need to redefine (if user hasnt chosen a file)
        if form.new_category.data:
            new_category = Category(form.new_category.data)
            db.session.add(new_category)
            db.session.flush()
            post.category = new_category
        db.session.commit()
        return redirect(url_for('article', slug=post.slug))
            
    return render_template('blog/post.html', form=form, post=post, action=edit) # pre loading post



@app.route('/delete/<int:post_id>') 
@author_required
def delete(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    post.live = False
    db.session.commit()
    flash("Article Deleted!")
    return redirect(url_for('admin'))
    

    