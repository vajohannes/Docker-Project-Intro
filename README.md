# Docker-Project-Intro

A series of beginner-friendly Docker projects to learn containerization, from basic web servers to multi-container applications. Each project builds upon the previous one, gradually increasing in complexity.

# 📋 Projects Overview

| Project Number | Name                              | Tools                        | Description                                      |
|:--------------:|-----------------------------------|------------------------------|--------------------------------------------------|
|        1       | Simple Nginx Web Server           | Docker, Nginx                | Containerized basic web server with port mapping |
|        2       | Python Script Containerization    | Docker, Python, pandas       | Containerized Python script with dependencies    |
|        3       | Multi-container Flask & MySQL App | Docker Compose, Flask, MySQL | Full-stack application with database             |

## 📁 Project 1: Simple Nginx Web Server

Learn: Basic Docker commands, port mapping, serving static content

```
my-nginx-project/
├── index.html
└── Dockerfile
```
## Quick Start

```bash
# Navigate to project directory
cd my-nginx-project

# Build the Docker image
docker build -t my-nginx-app .

# Run the container
docker run -d -p 8080:80 my-nginx-app

# Access the server
open http://localhost:8080
```
## Key Concepts

* Dockerfile syntax and instructions

* Image building with docker build

* Container port mapping

* Serving static HTML files




## 📁 Project 2: Dockerizing a Python Script

Learn: Dependency management, volume mounting, Python in containers

```
docker-python-project/
├── Dockerfile
├── requirements.txt
├── process_data.py
├── sales_data.csv
├── data.csv
└── Dockerfile.optimized
```

## Quick Start

```
# Navigate to project directory
cd docker-python-project

# Build the Docker image
docker build -t python-data-processor

# Run with sample data
docker run python-data-processor

# Run with custom data file
docker run -v $(pwd):/app python-data-processor python process_data.py sales_data.csv
```

## Key Concepts

* Managing Python dependencies in containers

* Using requirements.txt files

* Data persistence with volumes

* Multi-stage builds




## 📁 Project 3: Multi-container Flask & MySQL Application

Learn: Docker Compose, multi-service applications, database integration

```
flask-mysql-app/
├── docker-compose.yml
├── Dockerfile
├── app.py
├── static/
├── templates/
│   └── index.html
├── mysql-init/
│   └── 01-init.sql
└── requirements.txt
```

## Quick Start

```
# Navigate to project directory
cd flask-mysql-app

# Start all services with Docker Compose
docker-compose up --build

# Access the application
open http://localhost:5000

# Access phpMyAdmin (optional)
open http://localhost:8080
```

## Key Concepts

* Docker Compose for multi-container orchestration

* Service dependencies and networking

* Database initialization

* Environment variables configuration

* Volume persistence for databases


## 🛠️ Common Docker Commands Cheat Sheet

### Basic Commands

```
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# List Docker images
docker images

# Remove container
docker rm <container_name>

# Remove image
docker rmi <image_name>

# View logs
docker logs <container_name>

# Execute command in running container
docker exec -it <container_name> sh
```

### Build and Run

```
# Build image
docker build -t <image_name> .

# Run container
docker run -d -p <host_port>:<container_port> <image_name>

# Run with volume
docker run -v <host_path>:<container_path> <image_name>
```

### Docker Compose

```
# Start services
docker-compose up

# Start in background
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild images
docker-compose build

# List services
docker-compose ps
```

## 🔧 Troubleshooting

### Common Issues

1. "Port already in use"

```
# Find process using port
sudo lsof -i :<port>

# Or use different port
docker run -p 8081:80 <image_name>
```

2. "No space left on device"

```
# Clean up unused Docker objects
docker system prune -a
```

3. "Cannot connect to Docker daemon"

```
# Start Docker service (Linux)
sudo systemctl start docker

# Add user to docker group
sudo usermod -aG docker $USER
```

### Debug Commands

```
# Check Docker version
docker --version

# Check Docker Compose version
docker-compose --version

# Check container health
docker inspect <container_name>

# View resource usage
docker stats
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Report Bugs: Open an issue with detailed description

2. Suggest Features: Share your ideas for new projects

3. Improve Documentation: Fix typos or clarify instructions

4. Add Examples: Create more sample applications

### Contribution Guidelines

1. Fork the repository

2. Create a feature branch

3. Make your changes

4. Test thoroughly

5. Submit a pull request
