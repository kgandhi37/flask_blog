# access database

import os


SECRET_KEY = '\xd8\x94QH\xbej\xca9\x9a\xec\xab+\xec\xf6_\x86\xb6\x93\x9c_\xe1\x89z\xac'
DEBUG = True # to allow debugging and auto reload. Disable during production
# editing for docker now
DB_USERNAME = 'root'
DB_PASSWORD = 'test'
BLOG_DATABASE_NAME = 'blog'
DB_HOST = 'mysql:3306'
DB_URI = "mysql+pymysql://%s:%s@%s/%s" % (DB_USERNAME, DB_PASSWORD, DB_HOST, BLOG_DATABASE_NAME)
SQLALCHEMY_DATABASE_URI = DB_URI # note technically you can do all the above on one line here but seperate for readability
SQLALCHEMY_TRACK_MODIFICATIONS = True
# for image uploads:
UPLOADED_IMAGES_DEST = '/opt/flask_blog/static/images'
UPLOADED_IMAGES_URL = '/static/images/' # url to prepend any image we serve