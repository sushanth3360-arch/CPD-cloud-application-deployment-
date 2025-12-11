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
    Config for production on App Engine.

    By default, use DATABASE_URL if set (for Cloud SQL later).
    If it's not set, fall back to SQLite in /tmp, which is the only writable
    directory on App Engine Standard.
    """
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL")
        or "sqlite:////tmp/prod.db"
    )


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
