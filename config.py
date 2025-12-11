import os

from google.cloud import secretmanager

# Base directory of the project (folder where this config.py lives)
basedir = os.path.abspath(os.path.dirname(__file__))


def _get_db_password() -> str | None:
    """
    Try to get DB password from Secret Manager first (production),
    then fall back to DB_PASS env var.

    This is safe for local dev & Cloud Build because:
      - If GOOGLE_CLOUD_PROJECT or DB_PASS_SECRET_NAME are missing,
        or Secret Manager call fails, we just return DB_PASS.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    secret_name = os.environ.get("DB_PASS_SECRET_NAME")

    if project_id and secret_name:
        try:
            client = secretmanager.SecretManagerServiceClient()
            name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
            response = client.access_secret_version(name=name)
            return response.payload.data.decode("utf-8")
        except Exception:
            # In tests / local / misconfig, just fall back to env var
            pass

    return os.environ.get("DB_PASS")


class Config:
    """Base configuration shared by all environments."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        """Hook for any app-specific initialisation."""
        pass


class DevelopmentConfig(Config):
    """Config for local development (SQLite on disk)."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL")
        or "sqlite:///" + os.path.join(basedir, "dev.db")
    )


class ProductionConfig(Config):
    """
    Config for production on App Engine using Cloud SQL (MySQL).

    We expect:
      - DB_USER
      - DB_NAME
      - INSTANCE_CONNECTION_NAME
    For the password:
      - prefer Secret Manager via DB_PASS_SECRET_NAME
      - otherwise fall back to DB_PASS env var
    """

    DEBUG = False

    @staticmethod
    def _build_cloudsql_uri() -> str:
        db_user = os.environ.get("DB_USER")
        db_name = os.environ.get("DB_NAME")
        instance_conn_name = os.environ.get("INSTANCE_CONNECTION_NAME")

        db_pass = _get_db_password()

        if all([db_user, db_pass, db_name, instance_conn_name]):
            return (
                f"mysql+pymysql://{db_user}:{db_pass}"
                f"@/{db_name}?unix_socket=/cloudsql/{instance_conn_name}"
            )

        # Fallback – avoid hard crash if misconfigured
        return os.environ.get("DATABASE_URL") or "sqlite:////tmp/prod.db"

    SQLALCHEMY_DATABASE_URI = _build_cloudsql_uri.__func__()


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
