bootstrap:
	pip3 install -r requirements.txt
	python3 wsgi.py

dev:
	python3 wsgi.py

freeze:
	pip3 freeze > requirements.txt