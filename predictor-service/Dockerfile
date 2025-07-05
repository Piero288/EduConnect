FROM python:3.10-slim

WORKDIR /predictorservice

COPY . /predictorservice

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 9055

CMD ["python", "main.py"]
