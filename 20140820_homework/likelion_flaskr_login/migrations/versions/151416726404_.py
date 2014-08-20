"""empty message

Revision ID: 151416726404
Revises: None
Create Date: 2014-08-21 00:08:14.082000

"""

# revision identifiers, used by Alembic.
revision = '151416726404'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('join_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('article',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('author', sa.String(length=255), nullable=True),
    sa.Column('category', sa.String(length=255), nullable=True),
    sa.Column('like', sa.Integer(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('article_id', sa.Integer(), nullable=True),
    sa.Column('author', sa.String(length=255), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('like', sa.Integer(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['article_id'], ['article.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment')
    op.drop_table('article')
    op.drop_table('user')
    ### end Alembic commands ###