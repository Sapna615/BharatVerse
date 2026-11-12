# BharatVerse
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
python manage.py loaddata fixtures/initial_data.json  # Populates states, cultural entries, games & quizzes
python manage.py runserver
```

## 7. Docker (Production / Demo)
```bash
cp .env.example .env # Configure variables
docker compose up --build
```
Access at `http://localhost:8000`.

To run migrations and load initial data in Docker:
```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py loaddata fixtures/initial_data.json
```
To create a superuser for Curator access:
```bash
docker compose exec web python manage.py createsuperuser
```

## 8. Environment Variables
See `.env.example`. Ensure `SECRET_KEY` is secure, `DEBUG` is `False`, and `AI_API_KEY` is configured if bypassing Demo Mode.
