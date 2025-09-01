FROM python:3.10-slim

# Imposta directory di lavoro
WORKDIR /userservice

# Copia tutti i file nella directory corrente
COPY . /userservice

# Installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

# Espone la porta del servizio (9051 come deciso)
EXPOSE 9051

# Comando per avviare l'app Flask
CMD ["python", "main.py"]
