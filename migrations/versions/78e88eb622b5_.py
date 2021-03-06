"""empty message

Revision ID: 78e88eb622b5
Revises: 
Create Date: 2019-05-18 21:23:44.605289

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78e88eb622b5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('poll',
    sa.Column('name', sa.Enum('stratechery', 'startupboy', 'bryan_caplan_econlib', 'marginal_revolution', 'ribbonfarm', 'melting_asphalt', 'overcoming_bias', 'elaine_ou', 'eugene_wei', 'meaningness', 'cato', 'aei', 'brookings', 'niskanen', 'mercatus', 'pew', name='blogname'), nullable=False),
    sa.Column('last_time', sa.DateTime(), nullable=True),
    sa.Column('last_post', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('name')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('kindle_email', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_kindle_email'), 'user', ['kindle_email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('blog',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.Enum('stratechery', 'startupboy', 'bryan_caplan_econlib', 'marginal_revolution', 'ribbonfarm', 'melting_asphalt', 'overcoming_bias', 'elaine_ou', 'eugene_wei', 'meaningness', 'cato', 'aei', 'brookings', 'niskanen', 'mercatus', 'pew', name='blogname'), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('blog')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_kindle_email'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('poll')
    # ### end Alembic commands ###
