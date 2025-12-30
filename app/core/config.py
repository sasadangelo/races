# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
import os
from pathlib import Path
from typing import Any, ClassVar

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource
from pydantic_settings.main import SettingsConfigDict
from pydantic_settings.sources import YamlConfigSettingsSource

# Load .env file at module import
load_dotenv()


class AppConfig(BaseSettings):
    """Application configuration settings."""

    debug: bool = Field(default=True, description="Debug mode")
    host: str = Field(default="0.0.0.0", description="Host address")  # nosec B104
    port: int = Field(default=5001, description="Port number")
    secret_key: str | None = Field(default=None, description="Secret key from environment")

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(extra="ignore")


class DatabaseConfig(BaseSettings):
    """Database configuration settings."""

    relative_path: str = Field(default="instance/dev.db", description="Relative path to database")

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(extra="ignore")


class LogConfig(BaseSettings):
    """Logging configuration settings."""

    level: str = Field(default="INFO", description="Log level")
    console: bool = Field(default=True, description="Enable console logging")
    file: str | None = Field(default=None, description="Log file path")
    rotation: str = Field(default="10 MB", description="Log rotation size")
    retention: str = Field(default="7 days", description="Log retention period")
    compression: str = Field(default="zip", description="Log compression format")

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(extra="ignore")


class Settings(BaseSettings):
    """Main settings class that combines all configuration sections."""

    app: AppConfig
    database: DatabaseConfig
    log: LogConfig

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        yaml_file="config.yml",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """Customize settings sources: YAML file only."""
        return (
            YamlConfigSettingsSource(settings_cls),
            init_settings,
        )

    def model_post_init(self, __context: Any) -> None:
        """Load secret_key from environment after initialization."""
        # Try environment variable first, then .env file
        secret_key = os.getenv("APP_SECRET_KEY")
        if secret_key:
            self.app.secret_key = secret_key

    def get_database_uri(self) -> str:
        """Get the full database URI."""
        basedir: Path = Path(__file__).parent.parent.parent
        db_path: Path = basedir / self.database.relative_path
        return f"sqlite:///{db_path}"


# Load settings at module import
settings: Settings = Settings()  # type: ignore[call-arg]
