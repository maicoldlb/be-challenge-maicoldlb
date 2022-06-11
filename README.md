# FOOTBALL-API

Repository to get and save football data

## 1. Virtual environment

- Install global venv

  `python3 -m pip install venv`

- Create folder environment

  `mkdir .venv`

- Enter folder

  `cd .venv`

- Create virtual environment

  `python3 -m venv .`

- Activate virtual environment in path

  `.venv/bin/activate`

## 2. Install dependencies

- Install requirements

  `pip install -r requirements.txt --upgrade`

- Install development requirements

  `pip install -r requirements_dev.txt --upgrade`

## 3. Run

### 3.1 Application

- Local

  `python src/app.py`

- Docker
  `docker build -t football-api:1 .`

  `docker run -p 3000:3000 -it {image_number}`

### 3.2 Development libraries

- Run PyTest

  `python -m pytest src`

- Run flake8

  `python -m flake8 src`

- Run black

  `python -m black -l 120 src`

- Run isort

  `python -m isort -rc src`

- Run autoflake

  `python -m autoflake --in-place --remove-all-unused-imports -r src`

## 4. Swagger

- http://localhost:3000/#/
