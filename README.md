# EduConnect APP
## Descrizione

L’elaborato proposto si focalizza sulla progettazione ed implementazione di una piattaforma a microservizi, sviluppata per supportare la gestione di corsi erogati da una scuola che offre formazione linguistica ed informatica (es. corsi di inglese, francese, informatica, etc.). Il sistema consente agli studenti di registrarsi, iscriversi ai corsi di interesse e ricevere notifiche in tempo reale sui corsi d'interesse, tramite un meccanismo Pub/Sub implementato con Apache Kafka.
L’architettura si basa su un insieme di microservizi containerizzati con Docker e orchestrati tramite Kubernetes, ognuno con responsabilità specifiche: autenticazione, gestione utenti, gestione corsi, notifiche ed elaborazione predittiva delle metriche di sistema.  

## Prerequisiti
- [Docker](https://docs.docker.com/)
- [Kubernetes](https://kubernetes.io/docs/home/)

## Installazione su Docker

Se si desidera eseguire l'applicazione utilizzando Docker in un ambiente locale, seguire i seguenti passaggi:

1. **Clonare il repository:**

    ```bash
    git clone https://github.com/Piero288/EduConnect.git
    cd EduConnect
    ```

2. **Creare i files .env da inserire all'interno della root folder e della folder di ogni microservizio**
    
    ```bash
    notepad /EduConnect/.env
    # Inserire il valore delle seguenti variabili:
    #MYSQL_USERSERVICE_HOST=
    #MYSQL_USERSERVICE_DB=
    #MYSQL_COURSESERVICE_HOST=
    #MYSQL_COURSESERVICE_DB=
    #MYSQL_PORT=
    #MYSQL_USER=
    #MYSQL_PASSWORD=
    #MYSQL_ROOT_PASSWORD=
    ```
    ```bash
    notepad /EduConnect/api-gateway/.env
    # Inserire il valore delle seguenti variabili:
    #AUTH_SERVICE_URL=
    #USER_SERVICE_URL=
    #COURSE_SERVICE_URL=
    #PUBLISHER_SERVICE_URL=
    #PORT=
    ```
    ```bash
    notepad /EduConnect/auth-service/.env
    # Inserire il valore delle seguenti variabili:
    #JWT_SECRET=
    ```
    ```bash
    notepad /EduConnect/course-service/.env
    # Inserire il valore delle seguenti variabili:
    #MYSQL_HOST=
    #MYSQL_PORT=
    #MYSQL_DB=
    #MYSQL_USER=
    #MYSQL_PASSWORD=
    #MYSQL_ROOT_PASSWORD=
    #AUTH_SERVICE_URL=
    #ENVIRONMENT= "local || k8s"
    #KAFKA_BOOTSTRAP_SERVERS_K8S=
    #KAFKA_BOOTSTRAP_SERVERS_LOCAL=
    ```
    ```bash
    notepad /EduConnect/predictor-service/.env
    # Inserire il valore delle seguenti variabili:
    #PROMETHEUS_URL=
    ```
    ```bash
    notepad /EduConnect/publisher-service/.env
    # Inserire il valore delle seguenti variabili:
    #ENVIRONMENT= "local || k8s"
    #KAFKA_BOOTSTRAP_SERVERS_K8S=
    #KAFKA_BOOTSTRAP_SERVERS_LOCAL=
    ```
    ```bash
    notepad /EduConnect/subscriber-service/.env
    # Inserire il valore delle seguenti variabili:
    #ENVIRONMENT= "local || k8s"
    #KAFKA_BOOTSTRAP_SERVERS_K8S=
    #KAFKA_BOOTSTRAP_SERVERS_LOCAL=
    #TOPICS=
    #COURSE_SERVICE_URL=
    ```
    ```bash
    notepad /EduConnect/user-service/.env
    # Inserire il valore delle seguenti variabili:
    #MYSQL_HOST=
    #MYSQL_PORT=
    #MYSQL_DB=
    #MYSQL_USER=
    #MYSQL_PASSWORD=
    #MYSQL_ROOT_PASSWORD=
    #AUTH_SERVICE_URL=
    ```

3. **Buildare le immagini Docker:**

    ```bash
    # Esegui il build delle immagini per tutti i servizi
    docker-compose build
    ```

4. **Eseguire i container Docker:**

    ```bash
    docker-compose up -d
    ```

## Installazione Kubernetes

1. **Clonare il repository:**

   ```bash
   git clone https://github.com/Piero288/EduConnect.git
   ```

2. **Creare i file secret.yaml**
    Creare i file secret.yaml all'interno delle seguenti folder:
        - /EduConnect/k8s/user/01-auth-secret.yaml
        - /EduConnect/k8s/user/02-course-secret.yaml
        - /EduConnect/k8s/user/02-mysql-coursedb-secret.yaml
        - /EduConnect/k8s/user/02-user-secret.yaml
        - /EduConnect/k8s/user/02-mysql-userdb-secret.yaml

    In ogni file yaml bisogna riportare le varaibili presenti nei file .env del relativo microservizio ed usati in ambiente Docker.

3. **Configurazione del Cluster Kubernetes:**

    Assicurarsi di avere un cluster Kubernetes funzionante. Si possono utilizzare strumenti come Minikube.

4. **Configura il daemon docker di minikube e buildare le immagini**
    Eseguire lo script "build_all.bat" presente nella root folder

5. **Creare il namespace "educonnect" e applicare i Manifesti Kubernetes:**

    ```bash
    kubectl create namespace educonnect
    kubectl apply -f k8s/ --recursive
    ```

5. **Accesso ai Servizi:**

    Link utili: https://minikube.sigs.k8s.io/docs/start/

     ```
    Usando Minikube è possibile lanciare il seguente comando per riuscire a comunicare con il servizio.

     ```bash
     minikube tunnel
     ```
    
    - Per ottenere la dashboard su browser eseguire il comando:
   
    ```bash
     minikube dashboard
     ```

    - Per accedere a Prometheus da browser eseguire il comando per il port-foward:
    
    ```bash
     kubectl port-forward -n educonnect svc/prometheus 9090:9090
     ```

## Utilizzo

L'applicazione è ora in esecuzione sul proprio cluster Kubernetes. E' possibile interagire con i diversi servizi attraverso le loro rispettive API. Per informazioni dettagliate sull'utilizzo di ciascun servizio, consulta la documentazione dei singoli componenti, presente in "/EduConnect/docs/".
