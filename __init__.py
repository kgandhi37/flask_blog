from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy # importing SQLAlchemy
from flask.ext.migrate import Migrate
from flask.ext.markdown import Markdown
from flask_uploads.uploads import UploadSet, configure_uploads, IMAGES

app = Flask(__name__)
app.config.from_object('settings') # importing settings from a seperate file
db = SQLAlchemy(app) # to call db anywhere in project, db holds our database

#migrations - using migrate command

migrate = Migrate(app, db)

# markdown

Markdown(app) # application now knows how to render markdown

# images
uploaded_images = UploadSet('images', IMAGES) # defines what type of images going to be uploading and how to name that set
configure_uploads(app, uploaded_images)


from blog import views # go into home folder import views
from author import views