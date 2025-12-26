# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
import os
from pathlib import Path
from typing import ClassVar

import yaml
from pydantic import Field
from pydantic_settings import BaseSettings
from pydantic_settings.main import SettingsConfigDict


class AppConfig(BaseSettings):
    """Application configuration settings."""

    debug: bool = Field(default=True, description="Debug mode")
    host: str = Field(default="0.0.0.0", description="Host address")  # nosec B104
    port: int = Field(default=5001, description="Port number")
    secret_key: str | None = Field(default=None, description="Secret key from environment")

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_prefix="APP_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


class DatabaseConfig(BaseSettings):
    """Database configuration settings."""

    relative_path: str = Field(default="instance/dev.db", description="Relative path to database")

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(env_prefix="DB_", extra="ignore")


class Settings(BaseSettings):
    """Main settings class that combines all configuration sections."""

    app: AppConfig
    database: DatabaseConfig

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(extra="ignore")

    @classmethod
    def from_yaml(cls, config_path: str = "config.yml") -> "Settings":
        """Load settings from YAML file."""
        yaml_path: Path = Path(config_path)

        if not yaml_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {yaml_path}")

        with open(file=yaml_path) as f:
            config_data = yaml.safe_load(stream=f)

        # Load secret_key from environment
        secret_key: str | None = os.getenv("SECRET_KEY")
        if config_data.get("app"):
            config_data["app"]["secret_key"] = secret_key

        return cls(
            app=AppConfig(**config_data.get("app", {})),
            database=DatabaseConfig(**config_data.get("database", {})),
        )

    def get_database_uri(self) -> str:
        """Get the full database URI."""
        basedir: Path = Path(__file__).parent.parent.parent
        db_path: Path = basedir / self.database.relative_path
        return f"sqlite:///{db_path}"


# Load settings at module import
settings: Settings = Settings.from_yaml()
