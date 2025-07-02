FROM python:3.10-slim

WORKDIR /publisher

COPY . /publisher

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
