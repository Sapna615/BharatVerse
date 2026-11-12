import os

BASE_DIR = '/Users/sapnarai/BharatVerse'

# 1. Dockerfile
dockerfile = """FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    build-essential \\
    libpq-dev \\
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn psycopg2-binary python-dotenv

# Copy project
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "bharatverse.wsgi:application", "--bind", "0.0.0.0:8000"]
"""
with open(os.path.join(BASE_DIR, 'Dockerfile'), 'w') as f:
    f.write(dockerfile)

# 2. docker-compose.yml
docker_compose = """version: '3.8'

services:
  web:
    build: .
    command: gunicorn bharatverse.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db

  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_DB=bharatverse
      - POSTGRES_USER=bharatverse
      - POSTGRES_PASSWORD=bharatverse_pass
    ports:
      - "5432:5432"

volumes:
  postgres_data:
"""
with open(os.path.join(BASE_DIR, 'docker-compose.yml'), 'w') as f:
    f.write(docker_compose)

# 3. .dockerignore
dockerignore = """.git
.gitignore
.env
__pycache__
*.pyc
venv
.venv
node_modules
.idea
.vscode
media
staticfiles
"""
with open(os.path.join(BASE_DIR, '.dockerignore'), 'w') as f:
    f.write(dockerignore)

# 4. .env.example
env_example = """# Django settings
SECRET_KEY=change-me
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000

# Database
POSTGRES_DB=bharatverse
POSTGRES_USER=bharatverse
POSTGRES_PASSWORD=change-me
POSTGRES_HOST=db
POSTGRES_PORT=5432

# External Services
AI_API_KEY=
"""
with open(os.path.join(BASE_DIR, '.env.example'), 'w') as f:
    f.write(env_example)

# Create a local .env for testing
with open(os.path.join(BASE_DIR, '.env'), 'w') as f:
    f.write(env_example.replace('change-me', 'test-secret-key').replace('POSTGRES_HOST=db', 'POSTGRES_HOST=127.0.0.1'))

# 5. Update settings.py for Production Readiness
with open(os.path.join(BASE_DIR, 'bharatverse', 'settings.py'), 'r') as f:
    settings_content = f.read()

# Make sure we import os, dotenv
if "from dotenv import load_dotenv" not in settings_content:
    settings_content = "import os\\nfrom dotenv import load_dotenv\\nload_dotenv()\\n" + settings_content

if "STATIC_ROOT" not in settings_content:
    settings_content += "\\nSTATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')\\n"

with open(os.path.join(BASE_DIR, 'bharatverse', 'settings.py'), 'w') as f:
    f.write(settings_content)

# 6. Update README.md
readme_content = """# BharatVerse
**Discover India. Experience Culture. Preserve Heritage.**

## 1. Problem
**Problem Statement ID:** SIH26197
**Organization:** AICTE
**Category:** Heritage & Culture
**Problem:** Student Innovation-Ideas that showcase the rich cultural heritage and traditions of India.

## 2. Solution
BharatVerse is a comprehensive digital cultural ecosystem. It moves beyond static information by allowing users to explore, personalize, test their knowledge, and actively preserve their community's heritage in an interactive, visually immersive environment.

## 3. Key Features
- **Cultural Explorer:** Interactive map and regional filters.
- **Cultural Fingerprint:** Visual analytics of cultural composition.
- **Cultural Connections:** Discover how regions influence each other.
- **Virtual Museum:** A curated digital walk through India's living heritage.
- **Cultural Calendar:** Explore festivals and events chronologically.
- **Cultural Journeys:** Build and track personalized cultural itineraries.
- **Gamification:** Earn XP, unlock achievements, and level up by learning.
- **Community Preservation:** "Preserve a Tradition" community submission engine.
- **Curator Moderation:** Secure dashboard to review and publish community stories.
- **BharatVerse AI:** An integrated AI cultural guide featuring Demo Mode.

## 4. Technology
- Python, Django, Django REST Framework
- PostgreSQL
- Tailwind CSS, JavaScript (Vanilla)
- Docker, Gunicorn

## 5. Architecture
BharatVerse uses a modular Django architecture with isolated apps (`culture`, `exploration`, `gamification`, `contributions`, etc.). The frontend utilizes a globally consistent Tailwind design system. Community contributions pass through a secure moderation state machine before becoming public. The AI assistant relies on a context builder isolating verified BharatVerse knowledge.

## 6. Installation (Local Development)
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env # Update as needed
python manage.py migrate
python manage.py runserver
```

## 7. Docker (Production / Demo)
```bash
cp .env.example .env # Configure variables
docker compose up --build
```
Access at `http://localhost:8000`.

To run migrations in Docker:
```bash
docker compose exec web python manage.py migrate
```
To create a superuser for Curator access:
```bash
docker compose exec web python manage.py createsuperuser
```

## 8. Environment Variables
See `.env.example`. Ensure `SECRET_KEY` is secure, `DEBUG` is `False`, and `AI_API_KEY` is configured if bypassing Demo Mode.
"""
with open(os.path.join(BASE_DIR, 'README.md'), 'w') as f:
    f.write(readme_content)
