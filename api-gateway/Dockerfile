# Immagine base leggera con Python 3.10
#FROM python:3.10-slim
FROM python:3.10

# Imposta la directory di lavoro nel container
WORKDIR /apigateway

# Copia tutti i file nella working dir del container
COPY . /apigateway

# Installa le dipendenze Python
RUN pip install --no-cache-dir -r requirements.txt

# Esponi la porta su cui gira Flask
EXPOSE 5000

# Comando per avviare l'app
CMD ["python", "main.py"]
