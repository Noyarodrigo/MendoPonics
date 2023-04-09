#!/bin/bash

# Actualiza los repositorios del sistema
sudo apt update

# Instala los paquetes necesarios para que el sistema pueda descargar paquetes a través de HTTPS
sudo apt install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common

# Descarga y agrega la clave GPG oficial de Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# Añade el repositorio de Docker al sistema
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# Actualiza los repositorios del sistema una vez más
sudo apt update

# Instala Docker
sudo apt install -y docker-ce docker-ce-cli containerd.io

# Instala Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Concede permisos de ejecución al binario de Docker Compose
sudo chmod +x /usr/local/bin/docker-compose

# Verifica que Docker y Docker Compose hayan sido instalados correctamente
docker --version
docker-compose --version
