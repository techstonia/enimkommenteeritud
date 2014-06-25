#!flask/bin/python
from app import app
from app.parse import parse_sites, update_all_sites

parse_sites()
update_all_sites()