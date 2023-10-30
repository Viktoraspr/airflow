# vipranc-DE2.2

# Introduction

With this project, you can create DB, retrieve data using API to DB, and also there are several functions for analytic information requiring. 

It requires Python >=3.9

# Development

## Writing source code

Consider follow:
* [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

## Installation

Create a virtual environment:

    python -m venv .venv

Install package:

    pip install -r requirements.txt

# Project structure


src/constants/credentials.py - need to add credentials of Postgres DB.

1. Install docker desktop application if you don't have docker running on your machine
- [Download Docker Desktop Application for Mac OS](https://hub.docker.com/editions/community/docker-ce-desktop-mac)
- [Download Docker Desktop Application for Windows](https://hub.docker.com/editions/community/docker-ce-desktop-windows)
- 
1. Launch airflow by docker-compose
```bash
docker-compose up -d
```
1. Check the running containers
```bash

docker ps
```
1. Open browser and type http://0.0.0.0:8080 to launch the airflow webserver
