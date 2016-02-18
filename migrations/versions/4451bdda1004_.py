"""empty message

Revision ID: 4451bdda1004
Revises: 62bd04056fe5
Create Date: 2016-02-18 16:14:52.573315

"""

# revision identifiers, used by Alembic.
revision = '4451bdda1004'
down_revision = '62bd04056fe5'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('comment_body', sa.Text(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('comment_author_id', sa.Integer(), nullable=True),
    sa.Column('comment_date', sa.DateTime(), nullable=True),
    sa.Column('live', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['comment_author_id'], ['author.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.alter_column(u'author', 'is_author',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=True)
    op.alter_column(u'post', 'live',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=True)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(u'post', 'live',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.alter_column(u'author', 'is_author',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.drop_table('comment')
    ### end Alembic commands ###
