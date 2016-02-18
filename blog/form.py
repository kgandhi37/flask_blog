from flask_wtf import Form
from wtforms import validators, StringField, TextAreaField
from author.form import RegisterForm
from blog.models import Category
from wtforms.ext.sqlalchemy.fields import QuerySelectField # defining QuerySelectFields
from flask_wtf.file import FileField, FileAllowed

class SetupForm(RegisterForm): # RegisterForm is subclass of Form so works. Allows us to user username, fullname etc stops us repeating ourselves
    name = StringField('Blog name', [
        validators.Required(),
        validators.Length(max=80)
        ])
        
# defining categories for the PostForm below

def categories():
    return Category.query

# posting posts form
class PostForm(Form):
    image = FileField('Image', validators=[
        FileAllowed(['jpg','png'],'JPG and PNG images only!')
        ])
    title = StringField('Title', [
        validators.Required(),
        validators.Length(max=80)
        ])
    body = TextAreaField('Content', validators=[validators.Required()])
    category = QuerySelectField('Category', query_factory=categories, allow_blank=True)  # queryselectfield will make a select from a query from contents of a table
    new_category = StringField('New Category') # Allow to create new category if wanted

class CommentForm(Form):
    comment_body = TextAreaField('Comment', validators=[validators.Required()])