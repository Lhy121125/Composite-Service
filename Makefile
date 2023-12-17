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
	aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 149601685977.dkr.ecr.us-east-2.amazonaws.com
	docker build -t composite-service .
	docker tag composite-service:latest 149601685977.dkr.ecr.us-east-2.amazonaws.com/composite-service:latest
	docker push 149601685977.dkr.ecr.us-east-2.amazonaws.com/composite-service:latest
	

all: install lint test format deploy