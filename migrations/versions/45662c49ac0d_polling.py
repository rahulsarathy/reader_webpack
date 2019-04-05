"""Polling

Revision ID: 45662c49ac0d
Revises: 7eddada9c4ce
Create Date: 2019-04-04 12:51:34.154455

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45662c49ac0d'
down_revision = '7eddada9c4ce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('poll',
    sa.Column('name', sa.Enum('stratechery', 'startupboy', 'bryan_caplan_econlib', 'marginal_revolution', 'ribbonfarm', 'melting_asphalt', 'overcoming_bias', 'elaine_ou', 'eugene_wei', 'meaningness', 'cato', 'aei', 'brookings', 'niskanen', 'mercatus', 'pew', name='blogname'), nullable=False),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('poll')
    # ### end Alembic commands ###