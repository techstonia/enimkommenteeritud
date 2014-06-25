from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
novelty = Table('novelty', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('url', String, nullable=False),
    Column('headline', String, nullable=False),
    Column('tags', String),
    Column('published_date', DateTime),
    Column('last_update', DateTime),
    Column('comments_count', Integer),
    Column('site', String),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['novelty'].columns['tags'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['novelty'].columns['tags'].create()
