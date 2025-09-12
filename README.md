# Vehicle Diagnostics System

A comprehensive Python + Flutter application for Peugeot 2008 vehicle diagnostics and mobile reporting.

## 🚗 Overview

This system connects to Peugeot 2008 vehicles via Bluetooth OBD-II adapters to collect diagnostic data and display comprehensive reports and alerts on mobile devices (iPhone first, then Android) with graphical visualizations.

## 🏗️ Architecture

- **Backend**: Python FastAPI with SQLAlchemy ORM
- **Mobile**: Flutter cross-platform app (iOS/Android)
- **Hardware**: ELM327 Bluetooth OBD-II adapters
- **Database**: SQLite (development), PostgreSQL (production)
- **Visualization**: FL Chart library for mobile data visualization

## 📁 Project Structure

```
├── api/                    # Python FastAPI backend
│   ├── src/
│   │   ├── models/        # SQLAlchemy data models
│   │   ├── services/      # Business logic layer
│   │   ├── api/          # REST API endpoints
│   │   └── main.py       # FastAPI application
│   ├── tests/            # API tests (contract, integration, unit)
│   ├── config/           # Configuration management
│   └── scripts/          # Database utilities
├── mobile/               # Flutter mobile application
│   ├── lib/
│   │   ├── models/       # Dart data models
│   │   ├── services/     # API and storage services
│   │   ├── screens/      # Flutter UI screens
│   │   └── widgets/      # Reusable components
│   └── test/            # Flutter tests
├── specs/               # Feature specifications and planning
└── docs/               # Project documentation
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Flutter 3.x SDK
- ELM327 Bluetooth OBD-II adapter
- Peugeot 2008 vehicle (2008+ model year)

### Backend Setup

```bash
cd api
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
python scripts/init_db.py
python -m uvicorn src.main:app --reload
```

### Mobile Setup

```bash
cd mobile
flutter pub get
flutter run -d "iPhone Simulator"  # or android
```

## 📋 Implementation Status

### ✅ Completed Features (15/64 tasks - 23.4%)

- **Project Setup**: Complete development environment
- **Data Models**: All SQLAlchemy models with validation
- **Vehicle API**: Registration, listing, detail endpoints
- **Database**: Schema with constraints and relationships
- **Mobile Foundation**: Flutter app structure
- **Testing**: TDD-compliant contract tests

### 🚧 Core Functionality Working

- ✅ Vehicle registration with VIN validation
- ✅ Vehicle listing with pagination
- ✅ Database schema with foreign keys
- ✅ API error handling and validation
- ✅ Configuration management

### 🔄 Next Implementation Steps

1. **Session Management**: Diagnostic session endpoints
2. **Data Collection**: System data endpoints and OBD integration
3. **Mobile Integration**: API client and screens
4. **Hardware Testing**: ELM327 Bluetooth connectivity
5. **Reports & Alerts**: Analysis and notification systems

## 🧪 Testing

### Backend Tests
```bash
cd api
pytest tests/contract/ -v     # Contract tests
pytest tests/integration/ -v # Integration tests
pytest tests/unit/ -v        # Unit tests
```

### Mobile Tests
```bash
cd mobile
flutter test                 # Unit tests
flutter drive --target=test_driver/app.dart  # Integration tests
```

## 🔧 Configuration

Copy `.env.example` to `.env` and configure:

```bash
# Database
DB_TYPE=sqlite
DB_NAME=vehicle_diagnostics

# OBD Settings
OBD_ADAPTER_TYPE=ELM327
BT_DEVICE_NAME=OBDII
BT_PIN=1234

# API Settings
API_HOST=0.0.0.0
API_PORT=8000
```

## 📊 Key Features

### Vehicle Management
- VIN validation and registration
- Model year and specification tracking
- Vehicle statistics and history

### Diagnostic Sessions
- Bluetooth OBD-II connectivity
- Real-time data collection
- Session status management

### Data Visualization
- Fuel consumption analysis
- Error code reporting
- Performance metrics charts
- Mobile-optimized dashboards

### Alert System
- Critical issue notifications
- Maintenance reminders
- Severity-based prioritization

## 🛠️ Development

### Technology Stack

**Backend**:
- FastAPI (REST API framework)
- SQLAlchemy (ORM)
- python-obd (vehicle communication)
- Pydantic (data validation)
- Alembic (database migrations)

**Mobile**:
- Flutter (cross-platform framework)
- FL Chart (data visualization)
- Dio (HTTP client)
- SQLite (local storage)

**Testing**:
- pytest (Python testing)
- Flutter test framework
- Contract-driven development

### Code Quality

- **Linting**: Black, flake8, mypy for Python; flutter_lints for Dart
- **Testing**: TDD approach with comprehensive test coverage
- **Documentation**: OpenAPI specifications and inline documentation
- **Version Control**: Git with conventional commits

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Follow TDD: Write tests first, then implementation
4. Commit changes (`git commit -m 'Add amazing feature'`)
5. Push to branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## 📞 Support

For support and questions:
- Check the [issues](https://github.com/dmartinol/my-vehicle/issues) page
- Review the [documentation](./docs/)
- Follow the [quickstart guide](./specs/001-i-wanto-to/quickstart.md)

## 🔮 Roadmap

- [ ] Complete session management and data collection
- [ ] Mobile app with full feature parity
- [ ] Real-time data streaming
- [ ] Advanced diagnostic algorithms
- [ ] Multi-vehicle fleet management
- [ ] Cloud synchronization and backup
- [ ] Predictive maintenance analytics

---

**Status**: Active Development | **Version**: 1.0.0-alpha | **Last Updated**: 2025-09-12