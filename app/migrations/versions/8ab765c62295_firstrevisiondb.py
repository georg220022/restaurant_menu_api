"""FirstRevisionDB

Revision ID: 8ab765c62295
Revises: 
Create Date: 2023-01-20 05:20:25.904210

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '8ab765c62295'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('RestaurantMenu',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=2048), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_RestaurantMenu_id'), 'RestaurantMenu', ['id'], unique=False)
    op.create_table('RestaurantSubMenu',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('menu_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=2048), nullable=False),
    sa.ForeignKeyConstraint(['menu_id'], ['RestaurantMenu.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('RestaurantDish',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sub_menu_id', sa.Integer(), nullable=False),
    sa.Column('price', sa.Float(precision=2, asdecimal=True, decimal_return_scale=2), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=2048), nullable=False),
    sa.ForeignKeyConstraint(['sub_menu_id'], ['RestaurantSubMenu.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('RestaurantDish')
    op.drop_table('RestaurantSubMenu')
    op.drop_index(op.f('ix_RestaurantMenu_id'), table_name='RestaurantMenu')
    op.drop_table('RestaurantMenu')
    # ### end Alembic commands ###
