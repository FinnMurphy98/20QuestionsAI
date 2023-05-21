"""errors with previous scrips, had to start fresh

Revision ID: ac3dfb63205b
Revises: 
Create Date: 2023-05-21 10:29:32.175800

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac3dfb63205b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('User',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=128), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('User', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_User_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_User_username'), ['username'], unique=True)

    op.create_table('Game',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('role', sa.String(length=64), nullable=False),
    sa.Column('winner', sa.Boolean(), nullable=True),
    sa.Column('finished', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('Game', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_Game_timestamp'), ['timestamp'], unique=False)

    op.create_table('Message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('game_id', sa.Integer(), nullable=False),
    sa.Column('role', sa.String(length=64), nullable=False),
    sa.Column('content', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['game_id'], ['Game.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('Message', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_Message_timestamp'), ['timestamp'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Message', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_Message_timestamp'))

    op.drop_table('Message')
    with op.batch_alter_table('Game', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_Game_timestamp'))

    op.drop_table('Game')
    with op.batch_alter_table('User', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_User_username'))
        batch_op.drop_index(batch_op.f('ix_User_email'))

    op.drop_table('User')
    # ### end Alembic commands ###