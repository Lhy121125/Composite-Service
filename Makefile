install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt
	
lint:
	pylint --disable=R,C *.py

test:
	python -m unittest test_service.py

format:
	black *.py

deploy:
	echo "deploy goes here"

all: install lint test format deploye