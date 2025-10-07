## Setup
1. Create/activate the homework virtual environment: 
- python -m venv .venvHW2 
- devEDU: source .venvHW2/bin/activate
- windows: source .venvHW2/Scripts/activate

2. Install dependencies: pip install -r requirements.txt

3. Apply database migrations and seed data (optional fixtures pending): 
- cd homework2/Bookings/
- python manage.py migrate

4. Run the development server: 
- cd homework2/Bookings/
- python manage.py runserver 0.0.0.0:3000


## Testing
- Run the suite with: python manage.py test

## AI Use

- I used AI (chatGTP Codex) to help create the main page by explaing how to certain bootstrap effects and make edits to html/bootstrap that I dont know off of my head.

- Used Ai to explain how to setup serializers.py

- Used Ai to create SVG Logo

- Used Ai To help write tests

- Used AI to help create the seat selection menu. I wanted it to be intuitive

- Used AI to create user auth setup

