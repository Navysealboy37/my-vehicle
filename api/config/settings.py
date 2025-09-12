"""
Configuration settings for Vehicle Diagnostics API
Handles environment variables and application configuration
"""

import os
from typing import Optional, List
from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path


class DatabaseSettings(BaseSettings):
    """Database configuration settings"""
    
    type: str = Field(default="sqlite", env="DB_TYPE")
    host: str = Field(default="localhost", env="DB_HOST")
    port: int = Field(default=5432, env="DB_PORT")
    user: str = Field(default="postgres", env="DB_USER")
    password: str = Field(default="", env="DB_PASSWORD")
    name: str = Field(default="vehicle_diagnostics", env="DB_NAME")
    
    @property
    def url(self) -> str:
        """Generate database URL based on type"""
        if self.type == "sqlite":
            db_path = Path(__file__).parent.parent / "data" / f"{self.name}.db"
            db_path.parent.mkdir(exist_ok=True)
            return f"sqlite:///{db_path}"
        elif self.type == "postgresql":
            return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
        else:
            raise ValueError(f"Unsupported database type: {self.type}")


class OBDSettings(BaseSettings):
    """OBD-II connection settings"""
    
    adapter_type: str = Field(default="ELM327", env="OBD_ADAPTER_TYPE")
    connection_timeout: int = Field(default=30, env="OBD_CONNECTION_TIMEOUT")
    read_timeout: int = Field(default=10, env="OBD_READ_TIMEOUT")
    fast_mode: bool = Field(default=False, env="OBD_FAST_MODE")
    
    # Bluetooth settings
    bluetooth_device_name: str = Field(default="OBDII", env="BT_DEVICE_NAME")
    bluetooth_address: Optional[str] = Field(default=None, env="BT_ADDRESS")
    bluetooth_pin: str = Field(default="1234", env="BT_PIN")


class FirebaseSettings(BaseSettings):
    """Firebase/Firestore configuration"""
    
    project_id: str = Field(default="", env="FIREBASE_PROJECT_ID")
    credentials_path: Optional[str] = Field(default=None, env="FIREBASE_CREDENTIALS_PATH")
    collection_prefix: str = Field(default="dev", env="FIREBASE_COLLECTION_PREFIX")


class InfluxDBSettings(BaseSettings):
    """InfluxDB time-series database settings"""
    
    url: str = Field(default="http://localhost:8086", env="INFLUXDB_URL")
    token: str = Field(default="", env="INFLUXDB_TOKEN")
    org: str = Field(default="vehicle-diagnostics", env="INFLUXDB_ORG")
    bucket: str = Field(default="sensor-data", env="INFLUXDB_BUCKET")


class APISettings(BaseSettings):
    """API server configuration"""
    
    title: str = "Vehicle Diagnostics API"
    description: str = "API for Peugeot 2008 vehicle diagnostic data collection and mobile reporting"
    version: str = "1.0.0"
    
    host: str = Field(default="0.0.0.0", env="API_HOST")
    port: int = Field(default=8000, env="API_PORT")
    reload: bool = Field(default=True, env="API_RELOAD")
    
    # CORS settings
    allowed_origins: List[str] = Field(default=["*"], env="ALLOWED_ORIGINS")
    allowed_methods: List[str] = Field(default=["*"], env="ALLOWED_METHODS")
    allowed_headers: List[str] = Field(default=["*"], env="ALLOWED_HEADERS")


class SecuritySettings(BaseSettings):
    """Security and authentication settings"""
    
    secret_key: str = Field(default="dev-secret-key", env="SECRET_KEY")
    algorithm: str = Field(default="HS256", env="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")


class LoggingSettings(BaseSettings):
    """Logging configuration"""
    
    level: str = Field(default="INFO", env="LOG_LEVEL")
    format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        env="LOG_FORMAT"
    )
    file_path: Optional[str] = Field(default=None, env="LOG_FILE_PATH")


class Settings(BaseSettings):
    """Main application settings"""
    
    # Environment
    environment: str = Field(default="development", env="ENVIRONMENT")
    debug: bool = Field(default=True, env="DEBUG")
    
    # Component settings
    database: DatabaseSettings = DatabaseSettings()
    obd: OBDSettings = OBDSettings()
    firebase: FirebaseSettings = FirebaseSettings()
    influxdb: InfluxDBSettings = InfluxDBSettings()
    api: APISettings = APISettings()
    security: SecuritySettings = SecuritySettings()
    logging: LoggingSettings = LoggingSettings()
    
    # Performance settings
    max_concurrent_sessions: int = Field(default=10, env="MAX_CONCURRENT_SESSIONS")
    data_retention_days: int = Field(default=730, env="DATA_RETENTION_DAYS")  # 2 years
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings (dependency injection for FastAPI)"""
    return settings