# Deployment Guide (Firebase Hosting + Cloud Run)

## Reality check
- **Netlify** is best for static sites (and serverless functions). A full **server-rendered Django app** is not a native Netlify hosting target.
- **Firebase Hosting** can serve static content and can also route requests to **Cloud Run** for dynamic backends.

So: **Deploy Django to Cloud Run**, then use **Firebase Hosting** as your domain/CDN with rewrites to Cloud Run.

## 1) Create a Google Cloud / Firebase project
1. Create a Firebase project (this also creates/links a Google Cloud project).
2. Enable billing (Cloud Run requires it).

## 2) Create a Postgres database (recommended)
Use one of:
- Cloud SQL for PostgreSQL (Google)
- Or a managed Postgres like Supabase/Neon/Render

You will need a DATABASE_URL like:
postgres://USER:PASSWORD@HOST:5432/DBNAME

## 3) Deploy Django to Cloud Run (container)
### A) Install & login
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
gcloud services enable run.googleapis.com cloudbuild.googleapis.com
```

### B) Build & deploy
From the project folder:

```bash
gcloud run deploy biztrack-web \
  --source . \
  --region asia-south1 \
  --allow-unauthenticated \
  --set-env-vars DJANGO_DEBUG=0 \
  --set-env-vars DJANGO_ALLOWED_HOSTS=biztrack-web-xxxxx.a.run.app \
  --set-env-vars DJANGO_CSRF_TRUSTED_ORIGINS=https://YOUR_FIREBASE_DOMAIN \
  --set-env-vars DJANGO_SECRET_KEY="CHANGE_ME" \
  --set-env-vars DATABASE_URL="postgres://..."
```

After deploy, note the Cloud Run URL:
https://biztrack-web-xxxxx.a.run.app

### C) Run migrations (one-time)
Cloud Run itself is stateless. Run migrations using Cloud Build or locally against the same DATABASE_URL.

Local:
```bash
export DATABASE_URL="postgres://..."
python manage.py migrate
python manage.py createsuperuser
```

## 4) Firebase Hosting rewrite to Cloud Run
Firebase Hosting can rewrite all requests to your Cloud Run service.

### A) Initialize Hosting
```bash
npm i -g firebase-tools
firebase login
firebase init hosting
```

Choose:
- Use existing project: YOUR_PROJECT
- Public directory: firebase_public
- Configure as single-page app: No

### B) Configure rewrite (already included in firebase.json)
Edit `firebase.json`:
- serviceId: biztrack-web
- region: asia-south1

### C) Deploy hosting
```bash
firebase deploy --only hosting
```

Now your Firebase Hosting domain serves your Django app via Cloud Run.

## 5) Netlify (what you *can* do)
Netlify cannot run a long-lived Django server directly. What you *can* do:
- Host a static marketing site on Netlify (separate repo)
- Add a link/button to your Firebase/Cloud Run app
- Or reverse-proxy via Firebase Hosting (recommended) and skip Netlify for the app.

## 6) Production settings checklist
- Set `DJANGO_DEBUG=0`
- Set strong `DJANGO_SECRET_KEY`
- Set `DJANGO_ALLOWED_HOSTS` to your Cloud Run + Firebase custom domains
- Set `DJANGO_CSRF_TRUSTED_ORIGINS` to https://your-domain
- Use Postgres (don’t use SQLite in production)
- Configure file uploads:
  - For production, store uploads in Google Cloud Storage / S3-compatible storage

## 7) Admin hardening
- Create a non-admin staff group for regular users.
- Only Finance can access petty cash reconciliation.
- Only Managers can approve expenses.

(Implementing fine-grained permissions is straightforward using Django Groups + built-in permissions.)
