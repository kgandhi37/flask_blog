# views in flask is the controller. templates hold the view

from flask_blog import app, db
from flask import render_template, redirect, url_for, session, request, flash # session to store login, build this as you need more stuff
from author.form import RegisterForm, LoginForm # importing classes from form.py
from author.models import Author
from author.decorators import login_required
import bcrypt

@app.route('/login', methods=('GET','POST')) # @ is a decorator (modifier) basically modifies the function below it
def login():
    form = LoginForm() # calling LoginForm
    error = None
    
    if request.method == 'GET' and request.args.get('next'):
        session['next'] = request.args.get('next', None)
    if form.validate_on_submit(): # querying db for author with username and password
        author = Author.query.filter_by(
            username = form.username.data,
            ).first() # gets the first record - can use limit(1)
        if author:
            if bcrypt.hashpw(form.password.data, author.password) == author.password: # using bcrypt to check pass
                session['username'] = form.username.data
                session['is_author'] = author.is_author
                flash("User %s logged in" % form.username.data)
                if 'next' in session:
                    next = session.get('next')
                    session.pop('next')
                    return redirect(next)
                else:
                    return redirect(url_for('index'))
            else:
                error = "Incorrect username or password"
        else:
            error = "Incorrect username or password"
    return render_template('author/login.html', form=form, error=error)
    
    
@app.route('/register', methods=('GET','POST'))
def register():
    form = RegisterForm()
    if form.validate_on_submit(): # checking for valid form entry, on form.py we defined required fields, lengths etc
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(form.password.data, salt)
        author = Author(
            form.fullname.data,
            form.email.data,
            form.username.data,
            hashed_password,
            False
        )
        db.session.add(author)
        db.session.commit()
        flash("Author Registered!")
        return redirect(url_for('success'))
    return render_template('author/register.html', form=form)
    
@app.route('/success')
def success():
    return 'Author Registered!'
    
    
@app.route('/login_success')
@login_required
def login_success():
    return 'Logged in!'
    
@app.route('/logout')
@login_required
def logout():
    session.pop('username')
    session.pop('is_author')
    flash("User logged out")
    return redirect(url_for('index'))