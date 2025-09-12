# Data Model: Peugeot 2008 Vehicle Diagnostics and Mobile Reporting

## Core Entities

### Vehicle
Represents a Peugeot 2008 with diagnostic capabilities.

**Fields**:
- `id`: UUID - Unique vehicle identifier
- `vin`: String(17) - Vehicle Identification Number (required, unique)
- `model_year`: Integer - Manufacturing year (required)
- `engine_type`: String - Engine specification (e.g., "1.2L PureTech")
- `transmission`: String - Transmission type (manual/automatic)
- `created_at`: DateTime - Registration timestamp
- `updated_at`: DateTime - Last modification timestamp

**Validation Rules**:
- VIN must be exactly 17 characters, alphanumeric
- Model year must be between 2008-current year
- Engine type and transmission are optional but recommended

**Relationships**:
- One-to-many with DiagnosticSession
- One-to-many with Alert

### DiagnosticSession
Represents a single troubleshooting session with timestamps and connection status.

**Fields**:
- `id`: UUID - Unique session identifier
- `vehicle_id`: UUID - Foreign key to Vehicle (required)
- `started_at`: DateTime - Session start timestamp (required)
- `ended_at`: DateTime - Session end timestamp (nullable)
- `connection_method`: String - Connection type ("bluetooth", "wifi", "cable")
- `adapter_type`: String - Adapter model (e.g., "ELM327")
- `status`: Enum - Session status ("active", "completed", "failed", "interrupted")
- `total_data_points`: Integer - Number of data points collected
- `error_message`: String - Error description if status is "failed"
- `created_at`: DateTime - Record creation timestamp

**Validation Rules**:
- `ended_at` must be after `started_at` if present
- Status must be one of defined enum values
- Connection method required if status is "active" or "completed"

**State Transitions**:
- "active" → "completed" (normal completion)
- "active" → "failed" (connection/data error)
- "active" → "interrupted" (user cancellation)
- No transitions from "completed", "failed", or "interrupted"

**Relationships**:
- Many-to-one with Vehicle
- One-to-many with SystemData
- One-to-many with Report

### SystemData
Vehicle diagnostic information including error codes, sensor readings, and performance metrics.

**Fields**:
- `id`: UUID - Unique data point identifier
- `session_id`: UUID - Foreign key to DiagnosticSession (required)
- `timestamp`: DateTime - Data collection timestamp (required)
- `parameter_name`: String - OBD-II parameter name (e.g., "ENGINE_LOAD", "SPEED")
- `parameter_id`: String - OBD-II PID code (e.g., "01 04", "01 0D")
- `raw_value`: String - Raw value from vehicle
- `converted_value`: Float - Converted/calculated value
- `unit`: String - Unit of measurement (e.g., "km/h", "°C", "%")
- `is_error_code`: Boolean - True if this represents an error condition
- `severity_level`: Enum - Severity ("info", "warning", "error", "critical")

**Validation Rules**:
- Parameter name and ID must be from approved OBD-II standard list
- Converted value must be numeric if raw value contains numeric data
- Severity level required if is_error_code is true

**Relationships**:
- Many-to-one with DiagnosticSession

### Report
Formatted presentation of diagnostic findings with analysis and recommendations.

**Fields**:
- `id`: UUID - Unique report identifier
- `session_id`: UUID - Foreign key to DiagnosticSession (required)
- `report_type`: Enum - Type of report ("summary", "fuel_analysis", "error_analysis", "maintenance")
- `title`: String - Report title (required)
- `generated_at`: DateTime - Report generation timestamp (required)
- `summary`: Text - Executive summary of findings
- `recommendations`: JSON - Structured recommendations array
- `charts_config`: JSON - Chart configuration for mobile display
- `data_points_analyzed`: Integer - Number of data points used
- `status`: Enum - Report status ("generating", "ready", "archived")

**Validation Rules**:
- Title must be non-empty and under 200 characters
- Report type must be one of defined enum values
- Recommendations must be valid JSON array
- Charts config must be valid JSON object

**Relationships**:
- Many-to-one with DiagnosticSession
- One-to-many with Alert

### Alert
Critical notifications about vehicle issues requiring attention.

**Fields**:
- `id`: UUID - Unique alert identifier
- `vehicle_id`: UUID - Foreign key to Vehicle (required)
- `report_id`: UUID - Foreign key to Report (nullable)
- `alert_type`: Enum - Type of alert ("error_code", "maintenance", "performance", "safety")
- `severity`: Enum - Alert severity ("low", "medium", "high", "critical")
- `title`: String - Alert headline (required)
- `description`: Text - Detailed alert description
- `recommended_action`: Text - Suggested response to alert
- `is_acknowledged`: Boolean - User acknowledgment status (default: false)
- `created_at`: DateTime - Alert creation timestamp
- `acknowledged_at`: DateTime - User acknowledgment timestamp (nullable)
- `expires_at`: DateTime - Alert expiration (nullable)

**Validation Rules**:
- Title must be non-empty and under 100 characters
- Severity must be escalated based on alert type
- Acknowledged_at must be after created_at if present
- Expires_at must be after created_at if present

**Relationships**:
- Many-to-one with Vehicle
- Many-to-one with Report (optional)

### MobileDevice
User's smartphone or tablet for viewing reports and receiving alerts.

**Fields**:
- `id`: UUID - Unique device identifier
- `device_token`: String - Push notification token
- `platform`: Enum - Device platform ("ios", "android")
- `app_version`: String - Application version
- `os_version`: String - Operating system version
- `last_active`: DateTime - Last app usage timestamp
- `notification_preferences`: JSON - User notification settings
- `is_active`: Boolean - Device active status (default: true)

**Validation Rules**:
- Platform must be "ios" or "android"
- App version must follow semantic versioning
- Device token required for push notifications

**Relationships**:
- Many-to-many with Vehicle (via user association)

## Data Model Relationships

```
Vehicle (1) ──── (Many) DiagnosticSession
DiagnosticSession (1) ──── (Many) SystemData
DiagnosticSession (1) ──── (Many) Report
Report (1) ──── (Many) Alert
Vehicle (1) ──── (Many) Alert
MobileDevice (Many) ──── (Many) Vehicle
```

## Indexing Strategy

**Primary Indexes**:
- Vehicle: VIN (unique), model_year
- DiagnosticSession: vehicle_id, started_at, status
- SystemData: session_id, timestamp, parameter_name
- Report: session_id, report_type, generated_at
- Alert: vehicle_id, severity, created_at, is_acknowledged
- MobileDevice: device_token, platform, is_active

**Composite Indexes**:
- SystemData: (session_id, timestamp) for time-series queries
- Alert: (vehicle_id, is_acknowledged, severity) for notification filtering
- DiagnosticSession: (vehicle_id, status, started_at) for session history

## Data Retention Policy

- **SystemData**: 2 years for detailed diagnostic data
- **DiagnosticSession**: 5 years for warranty and maintenance history
- **Report**: 3 years for analysis and trend tracking
- **Alert**: 1 year after acknowledgment or resolution
- **Vehicle**: Permanent (until user deletion request)
- **MobileDevice**: 90 days after last activity