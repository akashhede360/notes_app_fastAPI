

# Notes App with FastAPI

A simple notes application built with **FastAPI** and **Uvicorn**, with the frontend served via **Nginx**. Supports creating, reading, updating, and deleting notes, and can be easily deployed using **Docker**.

## Features
- CRUD operations for notes
- FastAPI backend with Uvicorn
- Nginx for serving static frontend
- Dockerized for easy deployment

## Installation

Clone the repo:
```bash
git clone https://github.com/Akashhede/notes_app_fastAPI.git
cd notes_app_fastAPI


docker build -t notes_app .
docker run -p 8000:8000 notes_app
