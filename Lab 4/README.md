# Lab 4: FastAPI Docker Container

##  Introduction

This project demonstrates how to containerize a simple FastAPI service using Docker. It also includes remote access into the container for inspection and debugging purposes. The goal is to provide a foundational example of deploying Python web services using modern containerization techniques.

---

## Project Description

The FastAPI service provides a basic API endpoint (`/`) that returns a simple JSON message. This service is fully containerized using Docker, allowing it to be easily deployed, scaled, and managed in any environment that supports containers. 

This project covers:
- Writing a Dockerfile to containerize the FastAPI service
- Running the service in a Docker container
- Accessing the container remotely using an interactive shell

---

## Project Design

- **Docker**: Container platform to isolate and run the service.
- **Dockerfile**: Specifies the image and configuration needed to run the FastAPI app.
- **Requirements.txt**: Lists the Python dependencies (FastAPI and Uvicorn).


---

## How to Run the Project

### 1. Clone or Download the Project

```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Ensure Docker is Installed

Install Docker from: [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)

---

### 3. Build the Docker Image

```bash
docker build -t fastapi-docker .
```

---

### 4. Run the Docker Container

```bash
docker run -d -p 8000:8000 --name fastapi-container fastapi-docker
```

---

### 5. Test the FastAPI Service

Open your browser and go to:
```
http://localhost:8000
```

Or run:
```bash
curl http://localhost:8000
```
---

### 6. Remote Access into the Container

```bash
docker exec -it fastapi-container /bin/bash
```

You are now inside the container and can inspect the environment, run Python commands, or debug the application.

To exit the shell:
```bash
exit
```

---

### 7. Stop and Clean Up (Optional)

```bash
docker stop fastapi-container
docker rm fastapi-container
docker rmi fastapi-docker
```

---

## Summary

This project provides a hands-on example of how to containerize a FastAPI application and interact with it via Docker. It's an excellent starting point for learning about container-based deployment in Python web development.
