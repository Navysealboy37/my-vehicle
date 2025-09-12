# Quickstart Guide: Peugeot 2008 Vehicle Diagnostics

## Prerequisites

### Hardware Requirements
- Peugeot 2008 vehicle (2008+ model year)
- ELM327 Bluetooth OBD-II adapter
- Mobile device (iPhone iOS 15+ or Android 8+)
- Development machine with Python 3.11+

### Software Requirements
- Python 3.11+ with pip
- Flutter 3.x SDK
- Git for version control
- Code editor (VS Code recommended)

## Quick Setup (5 minutes)

### 1. Clone and Setup Backend
```bash
# Clone the repository
git clone <repository-url>
cd vehicle-diagnostics

# Create Python virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Initialize database
python scripts/init_db.py

# Start development server
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Setup Mobile Development
```bash
# Navigate to mobile app directory
cd mobile

# Install Flutter dependencies
flutter pub get

# Run on iOS simulator (macOS only)
flutter run -d "iPhone Simulator"

# Or run on Android emulator
flutter run -d android
```

### 3. Configure Hardware Connection
```bash
# Pair ELM327 adapter with development machine
# Find adapter in Bluetooth settings (usually appears as "OBDII" or "ELM327")
# Default PIN: 1234 or 0000

# Test connection
python scripts/test_connection.py --adapter-name "OBDII"
```

## First Diagnostic Session (10 minutes)

### Step 1: Register Your Vehicle
```bash
# Using API directly
curl -X POST http://localhost:8000/api/v1/vehicles \
  -H "Content-Type: application/json" \
  -d '{
    "vin": "VF3C9HHZE123456789",
    "model_year": 2020,
    "engine_type": "1.2L PureTech",
    "transmission": "manual"
  }'

# Response: {"id": "550e8400-e29b-41d4-a716-446655440000", ...}
```

### Step 2: Start Diagnostic Session
```bash
# Start session via API
curl -X POST http://localhost:8000/api/v1/vehicles/550e8400-e29b-41d4-a716-446655440000/sessions \
  -H "Content-Type: application/json" \
  -d '{
    "connection_method": "bluetooth",
    "adapter_type": "ELM327"
  }'

# Response: {"id": "session-uuid", "status": "active", ...}
```

### Step 3: Collect Vehicle Data
```bash
# Run diagnostic data collection
python scripts/collect_data.py \
  --session-id "session-uuid" \
  --duration 60 \
  --parameters "SPEED,RPM,ENGINE_LOAD,FUEL_LEVEL"

# Data will be automatically sent to API
```

### Step 4: Generate Report
```bash
# Generate fuel analysis report
curl -X POST http://localhost:8000/api/v1/sessions/session-uuid/reports \
  -H "Content-Type: application/json" \
  -d '{
    "report_type": "fuel_analysis",
    "title": "Fuel Consumption Analysis"
  }'

# Check report status
curl http://localhost:8000/api/v1/sessions/session-uuid/reports
```

### Step 5: View on Mobile App
1. Open the mobile app
2. Navigate to "Vehicles" tab
3. Select your Peugeot 2008
4. View "Latest Session" for diagnostic data
5. Check "Reports" for generated analysis
6. Review "Alerts" for any issues detected

## Validation Tests

### Backend API Tests
```bash
# Run all API tests
pytest tests/api/ -v

# Run specific endpoint tests
pytest tests/api/test_vehicles.py -v
pytest tests/api/test_sessions.py -v
pytest tests/api/test_reports.py -v
```

### Mobile App Tests
```bash
cd mobile

# Run unit tests
flutter test

# Run integration tests
flutter drive --target=test_driver/app.dart
```

### Hardware Integration Tests
```bash
# Test Bluetooth connection
python tests/integration/test_bluetooth.py

# Test OBD-II data collection
python tests/integration/test_obd_collection.py

# Test end-to-end workflow
python tests/integration/test_e2e_workflow.py
```

## Common Troubleshooting

### Bluetooth Connection Issues
```bash
# Check adapter status
hciconfig  # Linux
# or
system_profiler SPBluetoothDataType  # macOS

# Reset Bluetooth connection
sudo systemctl restart bluetooth  # Linux
# or manually unpair and re-pair adapter
```

### API Connection Issues
```bash
# Check server status
curl http://localhost:8000/health

# Check logs
tail -f logs/api.log

# Restart server
pkill -f uvicorn
python -m uvicorn api.main:app --reload
```

### Mobile App Issues
```bash
# Clean build cache
flutter clean
flutter pub get

# Check device connectivity
flutter devices

# Rebuild and run
flutter run --hot-reload
```

### Vehicle Connection Problems
```bash
# Test OBD-II port functionality
python scripts/test_obd_port.py

# Check supported PIDs
python scripts/list_supported_pids.py

# Verify vehicle compatibility
python scripts/check_vehicle_compatibility.py --vin "YOUR_VIN"
```

## Data Collection Examples

### Basic Engine Parameters
```bash
python scripts/collect_data.py \
  --session-id "session-uuid" \
  --parameters "RPM,SPEED,ENGINE_LOAD,COOLANT_TEMP" \
  --interval 1 \
  --duration 300
```

### Fuel Economy Analysis
```bash
python scripts/collect_data.py \
  --session-id "session-uuid" \
  --parameters "FUEL_LEVEL,MAF,SPEED,THROTTLE_POS" \
  --interval 5 \
  --duration 1800
```

### Error Code Scanning
```bash
python scripts/scan_errors.py \
  --session-id "session-uuid" \
  --clear-codes false
```

## Mobile App Features Demo

### Dashboard View
- Real-time vehicle status indicators
- Quick access to last diagnostic session
- Critical alerts prominently displayed
- Fuel consumption trends graph

### Reports Screen
- Historical diagnostic sessions
- Fuel economy analysis charts
- Maintenance recommendations
- Error code explanations

### Alerts Management
- Active alerts list with severity indicators
- Acknowledgment functionality
- Alert history and resolution tracking
- Push notification settings

## Next Steps

1. **Custom Parameters**: Configure additional OBD-II parameters for your specific Peugeot model
2. **Advanced Reports**: Create custom report templates for specific use cases
3. **Integration**: Connect with external services (maintenance tracking, parts ordering)
4. **Automation**: Set up scheduled diagnostic sessions and automated reporting
5. **Multi-Vehicle**: Add additional vehicles to your fleet

## Support

- **API Documentation**: http://localhost:8000/docs (when server is running)
- **Logs Location**: `logs/` directory
- **Configuration**: `config/` directory
- **Test Results**: `test_results/` directory

This quickstart guide should get you up and running with vehicle diagnostics in under 15 minutes. For advanced configuration and customization, refer to the detailed documentation in the `/docs` directory.