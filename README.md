# DHARA

A voice-first assistant that helps rural citizens in Hindi and Marathi.
It answers questions about government schemes, crop advice and health
from official documents, shows the source for every answer, and sends
emergencies straight to the right phone number.

## Team folders (nobody edits another person's folder)

- backend/  : Voice & AI (Person A)
- data/     : Data & Logic (Person B)
- frontend/ : UI & Demo (Person C)

## Run the backend (stub version)

1. cd backend
2. python -m venv .venv
3. .venv\Scripts\activate
4. python -m pip install -r requirements.txt
5. uvicorn app.main:app --reload
6. Open http://127.0.0.1:8000/docs

## Secrets

Copy .env.example to .env and put your own keys there.
Never upload the .env file to GitHub.