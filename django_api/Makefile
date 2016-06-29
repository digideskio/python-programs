deps:
	@pip install -r requirements.txt

test: deps
	@coverage run manage.py test 
	@coverage report --omit="*/tests/*,manage.py,django_api/settings.py" --include="./*" -m

run: deps
	@DEBUG=true ./manage.py runserver

