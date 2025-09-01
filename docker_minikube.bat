@echo off

echo Configuro Docker per usare il daemon di Minikube

FOR /f "delims=" %%i IN ('minikube -p minikube docker-env --shell cmd') DO %%i
pause