# SWE40006 Portfolio Task 4: Deploy Containers Using Docker

**Student:** <YadanarTheint>
**Student ID:** <104992813 / J22037276>
**Unit:** SWE40006 Software Deployment and Evolution
**Level attempted:** HD (Sub-tasks 4.1 to 4.4)

## Public Links

| Item | Link |
|---|---|
| Running web app (Task 4.3) | <public URL or IP, e.g. http://203.0.113.10> |
| GitHub repository | <this repo URL> |
| Docker Hub: hello-web | https://hub.docker.com/r/treasuretheint/hello-web |
| Docker Hub: moobit_pulse-app | https://hub.docker.com/r/treasuretheint/moobit_pulse-app |
| Docker Hub: text-analyser | https://hub.docker.com/r/treasuretheint/text-analyser |

## Repository Structure

```
.
├── README.md
├── hello-web/            # Task 4.2: Python hello-world web server
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── moobit_pulse-app/     # Task 4.3: new web app
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── docker-compose.yml
└── text-analyser/        # Task 4.4: non-web command-line app
    ├── analyser.py
    └── Dockerfile
```

Adjust folder names above to match your actual layout.

## Prerequisites

- Docker Desktop (Mac/Windows) or Docker Engine (Linux)
- A Docker Hub account (`docker login`)
- For multi-architecture builds: Docker Buildx (included with Docker Desktop)

## Task 4.1: Docker Setup and Hello-World

```bash
docker --version
docker login
docker run hello-world
docker images
docker ps -a
```

## Task 4.2: Python Hello-World Web Server

The Dockerfile starts from a bare Ubuntu image and installs the Python runtime manually, then runs a Flask web server on port 5000.

**Build and run**

```bash
cd hello-web
docker build -t treasuretheint/hello-web:v1 .
docker run -d -p 8080:5000 --name hello-web treasuretheint/hello-web:v1
curl http://localhost:8080
```

**Push and pull on another Docker device**

```bash
docker buildx create --use
docker buildx build --platform linux/amd64,linux/arm64 -t treasuretheint/hello-web:v1 --push .

# On the second device
docker pull treasuretheint/hello-web:v1
docker run -d -p 5000:5000 --name hello-web-pulled treasuretheint/hello-web:v1
```

A multi-platform build is used so the image runs on both amd64 (Codespaces, most cloud VMs) and arm64 (Apple Silicon).

## Task 4.3: New Web App (moobit_pulse-app)

A new Flask web application with persistent storage. A named volume (`notes_data`) keeps data after the container is removed.

**Build and run**

```bash
cd moobit_pulse-app
docker build -t treasuretheint/moobit_pulse-app:v1 .
docker run -d --restart unless-stopped -p 80:5000 -v notes_data:/data --name moobit_pulse-app treasuretheint/moobit_pulse-app:v1
docker ps
docker logs moobit_pulse-app
```

Open `http://localhost` (local) or the public URL listed above.

**Using Docker Compose (optional)**

```bash
docker compose up -d
docker compose down
```

**Persistence test**

```bash
docker rm -f moobit_pulse-app
docker run -d -p 80:5000 -v notes_data:/data --name moobit_pulse-app treasuretheint/moobit_pulse-app:v1
```

Data added earlier is still present after the new container starts.

## Task 4.4: Non-Web App (text-analyser)

A command-line Python program with no web server. It reads a text file from a mounted folder and prints line, word and character counts and the most common words. The container runs, prints its output and exits.

**Build and run**

```bash
cd text-analyser
docker build -t treasuretheint/text-analyser:v1 .
mkdir -p ~/input
echo "docker makes deployment easy and docker is fun" > ~/input/sample.txt
docker run --rm -v ~/input:/input treasuretheint/text-analyser:v1 /input/sample.txt --top 3
```

**Error handling demo (file not found)**

```bash
docker run --rm treasuretheint/text-analyser:v1 /input/missing.txt
```

## Troubleshooting Summary

| Error | Cause | Fix |
|---|---|---|
| `failed to read dockerfile: open Dockerfile: no such file or directory` | Build command run in a folder with no Dockerfile | `cd` into the correct folder, check with `ls` |
| `no matching manifest for linux/amd64/v3` | Image pushed from an arm64 machine only | Rebuilt with `docker buildx build --platform linux/amd64,linux/arm64 ... --push` |
| `no configuration file provided: not found` | `docker compose up` run without a compose file in the folder | Added `docker-compose.yml` or ran from the correct folder |
| `Conflict. The container name ... is already in use` | A container with the same name already existed | `docker rm -f <name>`, then re-ran |
| `http://172.17.0.3:5000` would not load | Internal Docker network IP is not reachable from outside | Used the published port (`localhost` or the public forwarded URL) 

## Cleanup

```bash
docker stop moobit_pulse-app hello-web
docker rm moobit_pulse-app hello-web
docker volume rm notes_data
```
