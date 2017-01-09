"""empty message

Revision ID: 9256c6e48cfe
Revises: 
Create Date: 2016-12-22 16:50:16.779127

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9256c6e48cfe'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Integer(), nullable=True),
    sa.Column('slug', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('slug')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=255), nullable=True),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('slug', sa.String(length=64), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('created_timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('slug')
    )
    op.create_table('entry',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('slug', sa.String(length=100), nullable=True),
    sa.Column('body', sa.Text(), nullable=False),
    sa.Column('status', sa.SmallInteger(), server_default='0', nullable=True),
    sa.Column('created_timestamp', sa.DateTime(), nullable=True),
    sa.Column('modified_timestamp', sa.DateTime(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('slug')
    )
    op.create_table('entry_tags',
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.Column('entry_is', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['entry_is'], ['entry.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('entry_tags')
    op.drop_table('entry')
    op.drop_table('user')
    op.drop_table('tag')
    # ### end Alembic commands ###