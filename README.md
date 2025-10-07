## Setup

1. Create/activate the homework virtual environment:
   ```bash
   python -m venv .venvHW2
   source .venvHW2/Scripts/activate  # Windows PowerShell
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Apply database migrations and seed data (optional fixtures pending):
   ```bash
   python manage.py migrate
   ```
4. Run the development server:
   ```bash
   python manage.py runserver 0.0.0.0:3000
   ```

## Functionality

- **REST API** (via Django REST Framework)
  - `GET /api/movies/` (CRUD enabled)
  - `GET /api/seats/` (read-only availability feed)
  - `GET|POST|DELETE /api/bookings/` (book seats, view, cancel history)
- **HTML UI**
  - Movie catalog with Bootstrap styling
  - Seat booking form (auth required) that ensures seat availability
  - Booking history page for the signed-in user

## Testing

- Model & API tests live in `home/tests.py`.
- Run the suite with:
  ```bash
  python manage.py test
  ```

## Deployment on Render

1. Commit the `render.yaml`, `Procfile`, and updated settings/requirements.
2. Push to GitHub and create a new Web Service on [Render](https://render.com/).
3. Select “Deploy from a repo”, choose this project, and Render will detect `render.yaml`.
4. Provision the generated PostgreSQL database and let Render run the build, collectstatic, and migrate commands defined in the blueprint.
5. Set `DJANGO_DEBUG` to `False` (already in `render.yaml`) and use the generated `DJANGO_SECRET_KEY`.
6. After the first deploy, visit the service URL; seat data is auto-seeded via migrations.

## AI Use

- ChatGPT (Codex) assisted with Bootstrap layout tweaks, logo SVG generation, and wiring Django views/templates/tests for the seat reservation workflow.
