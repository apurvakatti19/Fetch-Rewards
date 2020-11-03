app:
	python server.py
test:
	coverage run -m pytest test_server.py
packages:
	pip install -r requirements.txt