import os

# Base directory of the project (folder where this config.py lives)
basedir = os.path.abspath(os.path.dirname(__file__))


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

    We expect the following env vars to be set:
      - DB_USER
      - DB_PASS
      - DB_NAME
      - INSTANCE_CONNECTION_NAME

    This builds a SQLAlchemy URI using the Unix socket:
      mysql+pymysql://USER:PASS@/DB_NAME?unix_socket=/cloudsql/INSTANCE_CONNECTION_NAME

    If any of these are missing, we fall back to DATABASE_URL or a SQLite file in /tmp.
    """

    DEBUG = False

    @staticmethod
    def _build_cloudsql_uri() -> str:
        db_user = os.environ.get("DB_USER")
        db_pass = os.environ.get("DB_PASS")
        db_name = os.environ.get("DB_NAME")
        instance_conn_name = os.environ.get("INSTANCE_CONNECTION_NAME")

        if all([db_user, db_pass, db_name, instance_conn_name]):
            return (
                f"mysql+pymysql://{db_user}:{db_pass}"
                f"@/{db_name}?unix_socket=/cloudsql/{instance_conn_name}"
            )

        # Fallback – not ideal for production, but avoids hard crashes if misconfigured
        return os.environ.get("DATABASE_URL") or "sqlite:////tmp/prod.db"

    SQLALCHEMY_DATABASE_URI = _build_cloudsql_uri.__func__()


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
