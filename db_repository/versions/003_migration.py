from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
novelty = Table('novelty', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('url', String, nullable=False),
    Column('headline', String, nullable=False),
    Column('comments_count', Integer),
    Column('last_update', DateTime),
    Column('news_date', DateTime),
    Column('tags', String),
)

novelty = Table('novelty', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('url', String(length=2048), nullable=False),
    Column('headline', String(length=512), nullable=False),
    Column('tags', String(length=100)),
    Column('published_date', DateTime),
    Column('comments_count', Integer),
    Column('last_update', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['novelty'].columns['news_date'].drop()
    post_meta.tables['novelty'].columns['published_date'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['novelty'].columns['news_date'].create()
    post_meta.tables['novelty'].columns['published_date'].drop()
