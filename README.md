# Event Registration System — Auth & usage

This project supports:

- Web registration form (accounts/register/)
- Session (browsable) auth via DRF (`/api-auth/`)
- Token auth via `api-token-auth/` (POST) and `api/token/` (GET for logged-in users)

Quick examples

1. Web signup (recommended for new users)

- Open in browser: http://127.0.0.1:8000/accounts/register/
- After success you'll be redirected to the login provided by the browsable API: http://127.0.0.1:8000/api-auth/login/
- Login there and use the browsable API to register/cancel for events.

2. API signup (create user + token)

- Create a user and return token:
  curl -X POST -H "Content-Type: application/json" -d '{"username":"Jhapson","password":"secret","email":"a@b.com"}' http://127.0.0.1:8000/api/register/
  Response: {"username":"Jhapson","token":"<token>"}

3. Obtain token via credentials (existing DRF endpoint - POST only)

- The `api-token-auth/` endpoint only accepts POST (username & password). Example:
  curl -X POST -d "username=Jhapson&password=secret" http://127.0.0.1:8000/api-token-auth/

- If you try GET on that endpoint you will get "Method not allowed (GET)" — this is expected. Use POST.

4. Get token for currently logged-in user (session-auth)

- Login using browsable API (/api-auth/login/), then GET:
  curl -b cookiejar.txt -c cookiejar.txt http://127.0.0.1:8000/api/token/
  Response: {"token":"<token>"}

5. Use token to call protected endpoints:
   curl -H "Authorization: Token <token>" http://127.0.0.1:8000/api/events/

Admin UI

- Customize admin title via environment:
  - ADMIN_SITE_TITLE (default "E.R.S Admins")
  - ADMIN_INDEX_TITLE (default "JhapTech Administration")
- Example (PowerShell):
  $env:ADMIN_SITE_TITLE = "JhapTech Admin"

Notes

- The browsable API login is provided by `rest_framework.urls` at `/api-auth/` (login page).
- The `api-token-auth/` endpoint is for exchanging username/password for a token (POST only).
- `api/token/` added to allow session-authenticated users to obtain their token via GET.

Run migrations, create superuser, then create test users as needed:
$env:DJANGO_SETTINGS_MODULE = "config.settings.dev"
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
