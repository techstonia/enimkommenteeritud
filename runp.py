#!flask/bin/python
from app import app
from app.parse import parse_sites

parse_sites()
app.run(debug=False)