FROM python:3.10

WORKDIR /authentication
COPY . /authentication

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5002

CMD ["python", "main.py"]
