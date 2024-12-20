mig:
	./manage.py makemigrations
	./manage.py migrate
admin:
	python3 manage.py createsuperuser  --username admin --email  admin@mail.com

req:
	pip3 freeze > requirements.txt

install-req:
	pip3 install -r requirements.txt

static:
	python3 manage.py collectstatic

#   best artist,  bid, best_sellers,
# https://demo-egenslab.b-cdn.net/html/bidgen/preview/index-art-dark.html
# https://drawsql.app/teams/python-9/diagrams/aristo-auction




