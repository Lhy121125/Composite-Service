From python:3.9.16-slim-buster

RUN mkdir -p /app
COPY . main.py /app/
WORKDIR /app
RUN pip install -r requirements.py
EXPOSE 5001 
CMD ["main.py"]
ENTRYPOINT["python3"]