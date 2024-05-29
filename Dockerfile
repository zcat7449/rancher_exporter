FROM python:3.8

COPY . /app

WORKDIR /app
RUN pip install -r /app/requirements.txt

ENV PYTHONPATH '/app'

EXPOSE 8003

CMD ["python" , "/app/cluster5.py"]
