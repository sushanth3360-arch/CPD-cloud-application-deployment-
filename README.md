Flask To-Do List — Google Cloud Deployment (App Engine + Cloud SQL + CI/CD)

This project is a multi-user Flask to-do list app, but the main focus is real cloud deployment: the app runs on Google App Engine, stores data in Cloud SQL (MySQL), pulls secrets from Secret Manager, and deploys through Cloud Build (tests first, then deploys).

If you’re doing this as a cloud/devops-style project, this repo is set up to clearly demonstrate:

real managed database integration (Cloud SQL),

secret-handling (Secret Manager),

automated CI/CD (Cloud Build),

scalable hosting (App Engine).

Cloud architecture (what runs where)

App Engine (Python 3.11 + Gunicorn)
Hosts the Flask app and serves HTTP traffic.

Cloud SQL (MySQL)
Persistent database for users + tasks.

Secret Manager
Stores the database password securely (no hardcoding, no committing secrets).

Cloud Build
Runs pytest and deploys to App Engine if tests pass.

What you need before deploying
1) Google Cloud project requirements

A GCP project with billing enabled

APIs enabled:

App Engine

Cloud Build

Cloud SQL Admin

Secret Manager

2) Create Cloud SQL (MySQL)

You need a MySQL instance and a database.

Key value you’ll use later:

INSTANCE_CONNECTION_NAME
Format: PROJECT_ID:REGION:INSTANCE_NAME

3) Store DB password in Secret Manager

Create a secret that contains the DB password.

You’ll reference it later as:

DB_PASS_SECRET_NAME (secret name)

App Engine configuration

Deployment is controlled by app.yaml.

Important environment variables

These should exist in app.yaml (or be set in your deployment environment):

FLASK_ENV=production

DB_USER (Cloud SQL username)

DB_NAME (database name)

INSTANCE_CONNECTION_NAME (Cloud SQL connection name)

DB_PASS_SECRET_NAME (Secret Manager secret holding DB password)

SECRET_KEY (recommended — Flask session security)

Cloud SQL socket wiring

In production, the app connects using a Cloud SQL Unix socket (App Engine-friendly).
app.yaml also whitelists the instance via beta_settings.cloud_sql_instances.


CI/CD pipeline (Cloud Build)

Deployment is driven by cloudbuild.yaml.

Pipeline flow:

Use Python 3.11 build step

Install dependencies from requirements.txt
run tests
1. pytest -q
If tests pass → deploy:
gcloud app deploy app.yaml --quiet

How production configuration works (high-level)
config.py

Detects environment using FLASK_ENV

In production:

Fetches DB password from Secret Manager using:

GOOGLE_CLOUD_PROJECT (usually auto-available in GCP runtime)

DB_PASS_SECRET_NAME

Builds a Cloud SQL socket-based MySQL URI using:

DB_USER, DB_NAME, INSTANCE_CONNECTION_NAME

Falls back safely (for local/dev) to DB_PASS or SQLite when secrets aren’t available.

main.py

Loads the selected config

Initialises Flask + SQLAlchemy

Registers auth + todo blueprints

Creates tables on startup within app context (so first deploy boots cleanly)



Minimal local run (only for development)

If you just want to test locally, it runs with SQLite automatically:
python -m venv .venv
.\.venv\Scripts\Activate
pip install -r requirements.txt
flask --app main run --debug
