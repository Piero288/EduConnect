@echo off

echo Configuro Docker per usare il daemon di Minikube

FOR /f "delims=" %%i IN ('minikube -p minikube docker-env --shell cmd') DO %%i

echo Building auth-service...
docker build -t educonnect-auth-service:1.0.0 -f auth-service\Dockerfile auth-service

echo Building user-service...
docker build -t educonnect-user-service:1.0.0 -f user-service\Dockerfile user-service

echo Building course-service...
docker build -t educonnect-course-service:1.0.0 -f course-service\Dockerfile course-service

echo Building publisher-service...
docker build -t educonnect-publisher-service:1.0.0 -f publisher-service\Dockerfile publisher-service

echo Building subscriber-service...
docker build -t educonnect-subscriber-service:1.0.0 -f subscriber-service\Dockerfile subscriber-service

echo Building predictor-service...
docker build -t educonnect-predictor-service:1.0.0 -f predictor-service\Dockerfile predictor-service

echo Tutte le immagini sono state create correttamente per Minikube.
pause
