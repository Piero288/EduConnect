FROM python:3.10-slim

# Imposta directory di lavoro
WORKDIR /courseservice

# Copia tutti i file nella directory corrente
COPY . /courseservice

# Installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

# Espone la porta del servizio (9051 come deciso)
EXPOSE 9052

# Comando per avviare l'app Flask
CMD ["python", "main.py"]