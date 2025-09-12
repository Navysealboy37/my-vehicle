#!/usr/bin/env python3
"""
Database initialization script for Vehicle Diagnostics API
Creates necessary tables and initial data for the application
"""

import os
import sys
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_database_url() -> str:
    """Create database URL from environment variables or use default SQLite"""
    db_type = os.getenv("DB_TYPE", "sqlite")
    
    if db_type == "sqlite":
        db_path = Path(__file__).parent.parent / "data" / "vehicle_diagnostics.db"
        db_path.parent.mkdir(exist_ok=True)
        return f"sqlite:///{db_path}"
    elif db_type == "postgresql":
        host = os.getenv("DB_HOST", "localhost")
        port = os.getenv("DB_PORT", "5432")
        user = os.getenv("DB_USER", "postgres")
        password = os.getenv("DB_PASSWORD", "")
        database = os.getenv("DB_NAME", "vehicle_diagnostics")
        return f"postgresql://{user}:{password}@{host}:{port}/{database}"
    else:
        raise ValueError(f"Unsupported database type: {db_type}")


def init_database():
    """Initialize the database with tables and initial data"""
    try:
        # Create database URL
        database_url = create_database_url()
        logger.info(f"Initializing database: {database_url}")
        
        # Create engine
        engine = create_engine(database_url, echo=True)
        
        # Test connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            logger.info("Database connection successful")
        
        # Import models to register tables (will be created in future tasks)
        logger.info("Database models will be imported here when implemented")
        
        # For now, create a simple test table
        with engine.connect() as connection:
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS health_check (
                    id INTEGER PRIMARY KEY,
                    service_name VARCHAR(50) NOT NULL,
                    status VARCHAR(20) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            # Insert initial health check record
            connection.execute(text("""
                INSERT OR IGNORE INTO health_check (id, service_name, status)
                VALUES (1, 'vehicle-diagnostics-api', 'initialized')
            """))
            
            connection.commit()
        
        logger.info("Database initialization completed successfully")
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        sys.exit(1)


def check_database_connection():
    """Check if database connection is working"""
    try:
        database_url = create_database_url()
        engine = create_engine(database_url)
        
        with engine.connect() as connection:
            result = connection.execute(text("SELECT service_name, status FROM health_check WHERE id = 1"))
            row = result.fetchone()
            if row:
                logger.info(f"Database health check: {row[0]} - {row[1]}")
                return True
            else:
                logger.warning("No health check record found")
                return False
                
    except Exception as e:
        logger.error(f"Database connection check failed: {e}")
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Vehicle Diagnostics Database Initialization")
    parser.add_argument("--check", action="store_true", help="Check database connection")
    parser.add_argument("--init", action="store_true", help="Initialize database")
    
    args = parser.parse_args()
    
    if args.check:
        success = check_database_connection()
        sys.exit(0 if success else 1)
    elif args.init:
        init_database()
    else:
        # Default action: initialize
        init_database()