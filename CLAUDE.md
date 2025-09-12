# Vehicle Diagnostics Development Guidelines

Auto-generated from all feature plans. Last updated: 2025-09-12

## Active Technologies

**Language/Version**: Python 3.11+ (client application requirement)
**Primary Dependencies**: python-obd, Flutter, FastAPI/Flask, SQLite, Firestore, InfluxDB
**Storage**: Multi-tier (SQLite local + Firestore cloud + InfluxDB time-series + AWS S3 archival)
**Testing**: pytest (Python), Flutter test framework
**Target Platform**: Mobile (iPhone first, then Android) + Development environment
**Project Type**: mobile (Python backend API + mobile app frontends)

## Project Structure
```
# Mobile + API Architecture
api/
├── src/
│   ├── models/          # Data models (Vehicle, DiagnosticSession, etc.)
│   ├── services/        # Business logic (OBD connection, data processing)
│   └── api/            # REST API endpoints
└── tests/
    ├── contract/       # API contract tests
    ├── integration/    # Bluetooth + vehicle integration tests
    └── unit/          # Unit tests

ios/
└── [Flutter iOS app]

android/
└── [Flutter Android app]

specs/001-i-wanto-to/
├── plan.md            # Implementation plan
├── research.md        # Technical research findings
├── data-model.md      # Entity relationships and schema
├── quickstart.md      # Getting started guide
└── contracts/         # API specifications (OpenAPI)
```

## Commands

### Python Backend Development
```bash
# Setup development environment
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Start API server
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# Run tests (TDD enforced)
pytest tests/contract/ -v      # Contract tests first
pytest tests/integration/ -v  # Integration tests
pytest tests/unit/ -v         # Unit tests last

# Database operations
python scripts/init_db.py     # Initialize database
python scripts/migrate_db.py  # Run migrations

# Vehicle diagnostics
python scripts/test_connection.py --adapter-name "OBDII"
python scripts/collect_data.py --session-id "uuid" --duration 60
```

### Flutter Mobile Development
```bash
cd mobile

# Setup and dependencies
flutter pub get

# Development
flutter run -d "iPhone Simulator"  # iOS
flutter run -d android            # Android

# Testing
flutter test                      # Unit tests
flutter drive --target=test_driver/app.dart  # Integration tests

# Build and deployment
flutter build ios --release
flutter build apk --release
```

### Hardware Integration
```bash
# Bluetooth setup and testing
python scripts/test_bluetooth.py
python scripts/test_obd_port.py
python scripts/check_vehicle_compatibility.py --vin "VIN_NUMBER"

# Data collection examples
python scripts/scan_errors.py --session-id "uuid"
python scripts/collect_data.py --parameters "SPEED,RPM,ENGINE_LOAD"
```

## Code Style

### Python (Backend API)
- Use FastAPI for REST API with automatic OpenAPI generation
- SQLAlchemy for database ORM with Alembic migrations
- Pydantic for data validation and serialization
- python-obd library for vehicle communication
- Type hints required for all functions
- Black code formatting with 88 character line limit
- pytest for testing with real hardware (no mocking of Bluetooth/OBD)

### Flutter (Mobile Apps)
- Material Design 3 components for consistent UI
- FL Chart library for data visualizations (charts, graphs)
- Provider or Riverpod for state management
- Dio HTTP client for API communication with retry logic
- SQLite (sqflite) for local data storage and offline capability
- Test-driven development with widget and integration tests

### API Design Principles
- RESTful endpoints following OpenAPI 3.0 specification
- Consistent error responses with proper HTTP status codes
- Pagination for list endpoints (limit/offset)
- ISO 8601 datetime formatting
- UUID identifiers for all entities
- Validation of VIN numbers and OBD-II parameter codes

## Recent Changes

**Feature 001-i-wanto-to** (2025-09-12): Added Peugeot 2008 vehicle diagnostics and mobile reporting
- Research: python-obd + ELM327 for Bluetooth OBD-II connectivity
- Research: Flutter for cross-platform mobile with FL Chart for visualizations  
- Research: Multi-tier storage (SQLite + Firestore + InfluxDB + S3)
- Design: Complete data model with Vehicle, DiagnosticSession, SystemData, Report, Alert entities
- Contracts: RESTful API specification with vehicle registration, session management, data collection, reporting
- Architecture: Mobile + API structure with Python backend and Flutter frontend apps

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->