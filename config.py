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
    """Config for local development (SQLite)."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL")
        or "sqlite:///" + os.path.join(basedir, "dev.db")
    )


class ProductionConfig(Config):
    """Config for production on GCP (Cloud SQL via DATABASE_URL)."""
    DEBUG = False
    # In production we EXPECT DATABASE_URL to be set
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
