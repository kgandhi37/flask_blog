# Set the path (similar to manage.py)
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import sqlalchemy
from flask.ext.sqlalchemy import SQLAlchemy

from flask_blog import app, db

# models
from author.models import *
from blog.models import *

# test in classes (one or multiple)

class UserTest(unittest.TestCase): # have to be instance of TestCase
    # use setUp and tearDown here - setUp, temporary db so you don't use production db
    def setUp(self):
        # like setting.py
        # can read the config
        db_username = app.config['DB_USERNAME']
        db_password = app.config['DB_PASSWORD']
        db_host = app.config['DB_HOST']
        # not passing db name until later, see below
        self.db_uri = "mysql+pymysql://%s:%s@%s/" % (db_username, db_password, db_host)
        # telling flask that we are in test mode
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False # turns csrf for testing
        app.config['BLOG_DATABASE_NAME'] = 'test_blog'
        app.config['SQLALCHEMY_DATABASE_URI'] = self.db_uri + app.config['BLOG_DATABASE_NAME']
        engine = sqlalchemy.create_engine(self.db_uri) # creating engine
        conn = engine.connect() # connecting to engine
        conn.execute("commit") # execute commit anything on session gets cleared out
        conn.execute("CREATE DATABASE " + app.config['BLOG_DATABASE_NAME'])
        db.create_all() # creating tables
        conn.close()
        self.app = app.test_client()
        
    def tearDown(self):
        db.session.remove()
        engine = sqlalchemy.create_engine(self.db_uri) # creating engine
        conn = engine.connect() # connecting to engine
        conn.execute("commit") # execute commit anything on session gets cleared out
        conn.execute("DROP DATABASE " + app.config['BLOG_DATABASE_NAME'])
        conn.close()
    
    # function for creating blog as in each test we will need to create a blog so can be called in tests
    def create_blog(self):
        return self.app.post('/setup', data=dict(
            name='My Test Blog',
            fullname = 'Kishen Gandhi',
            email='kishen.gandhi.1990@gmail.com',
            username='kishen',
            password='test',
            confirm='test'
            ),
        follow_redirects=True) # allow it to follow redirects etc
        
    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
            ),
            follow_redirects=True)
            
    def logout(self):
        return self.app.get('/logout', follow_redirects=True) # using get here as don't need to post params
        
    def register_user(self, fullname, email, username, password, confirm):
        return self.app.post('/register', data=dict(
            fullname=fullname,
            email=email,
            username=username,
            password=password,
            confirm=confirm
            ),
        follow_redirects=True)

    def publish_post(self, title, body, category, new_category):
        return self.app.post('/post', data=dict(
            title=title,
            body=body,
            category=category,
            new_category=new_category,
            ),
        follow_redirects=True)
    
    
    
    
    def test_create_blog(self): # have to start a test with test so it tells python to run it
        rv = self.create_blog() # rv = return value
        # print(rv.data)
        assert 'Blog Created' in str(rv.data) # check if Blog Created is a string created if test runs properly. Here is an example of why we need redirects
        
    def test_login_logout(self):
        self.create_blog()
        rv = self.login('kishen', 'test') # user created above.
        assert 'User kishen logged in' in str(rv.data)
        rv = self.logout()
        assert 'User logged out' in str(rv.data)
        rv = self.login('kishen', 'wrong')
        assert 'Incorrect username or password' in str(rv.data)
        
    #this will fail below (at register) because rv string isnt being returned but works in general. Will look at this properly
        
    def test_admin(self):
        self.create_blog()
        self.login('kishen', 'test')
        rv = self.app.get('/admin', follow_redirects=True)
        assert 'Welcome, kishen' in str(rv.data)
        rv = self.logout()
        rv = self.register_user('John Doe', 'john@example.com', 'john', 'test', 'test')
        assert 'Author registered!' in str(rv.data)
        rv = self.login('john', 'test')
        assert 'User john logged in' in str(rv.data)
        rv = self.app.get('/admin', follow_redirects=True)
        assert "403 Forbidden" in str(rv.data)

if __name__ == '__main__':
    unittest.main() # will call the first test it finds. will initialise setup, run all tests and then teardown
    
    
        