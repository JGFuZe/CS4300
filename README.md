## Setup
1. Create/activate the homework virtual environment:
   ```bash
   python -m venv .venvHW2
   source .venvHW2/bin/activate       # DevEDU
   .\.venvHW2\Scripts\activate       # Windows PowerShell
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Apply database migrations and seed data (optional fixtures pending):
   ```bash
   cd homework2/Bookings/
   python manage.py migrate
   ```

4. Run the development server:
   ```bash
   cd homework2/Bookings/
   python manage.py runserver 0.0.0.0:3000
   ```

## Testing
- Run the suite with:
  ```bash
  python manage.py test
  ```

## AI Use

- I used AI (chatGTP Codex) to help create the main page by explaining how to apply certain Bootstrap effects and make edits to html/bootstrap that I don't know off the top of my head.
- Used AI to explain how to set up `serializers.py`.
- Used AI to create the SVG logo.
- Used AI to help write tests.
- Used AI to help create the seat selection menu; I wanted it to be intuitive.
- Used AI to create user auth setup.
