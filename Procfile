web: gunicorn runp-heroku:app
init: python db_create.py
upgrade: python db_upgrade.py
parse: python app/parse.py
test: python test.py