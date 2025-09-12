# Implementation Plan: Peugeot 2008 Vehicle Diagnostics and Mobile Reporting

**Branch**: `001-i-wanto-to` | **Date**: 2025-09-12 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-i-wanto-to/spec.md`

## Execution Flow (/plan command scope)
```
1. Load feature spec from Input path
   → If not found: ERROR "No feature spec at {path}"
2. Fill Technical Context (scan for NEEDS CLARIFICATION)
   → Detect Project Type from context (web=frontend+backend, mobile=app+api)
   → Set Structure Decision based on project type
3. Evaluate Constitution Check section below
   → If violations exist: Document in Complexity Tracking
   → If no justification possible: ERROR "Simplify approach first"
   → Update Progress Tracking: Initial Constitution Check
4. Execute Phase 0 → research.md
   → If NEEDS CLARIFICATION remain: ERROR "Resolve unknowns"
5. Execute Phase 1 → contracts, data-model.md, quickstart.md, agent-specific template file (e.g., `CLAUDE.md` for Claude Code, `.github/copilot-instructions.md` for GitHub Copilot, or `GEMINI.md` for Gemini CLI).
6. Re-evaluate Constitution Check section
   → If new violations: Refactor design, return to Phase 1
   → Update Progress Tracking: Post-Design Constitution Check
7. Plan Phase 2 → Describe task generation approach (DO NOT create tasks.md)
8. STOP - Ready for /tasks command
```

**IMPORTANT**: The /plan command STOPS at step 7. Phases 2-4 are executed by other commands:
- Phase 2: /tasks command creates tasks.md
- Phase 3-4: Implementation execution (manual or via tools)

## Summary
Develop a Python-based vehicle diagnostics application that connects to Peugeot 2008 vehicles via Bluetooth to retrieve system data for troubleshooting, then displays comprehensive reports and alerts on mobile devices (iPhone first, then Android) with graphical visualizations.

## Technical Context
**Language/Version**: Python 3.11+ (client application requirement)  
**Primary Dependencies**: NEEDS CLARIFICATION (Bluetooth library, mobile framework)  
**Storage**: NEEDS CLARIFICATION (local files, cloud storage, or embedded database)  
**Testing**: pytest (Python standard)  
**Target Platform**: Mobile (iPhone first, then Android) + Development environment  
**Project Type**: mobile (Python backend API + mobile app frontends)  
**Performance Goals**: NEEDS CLARIFICATION (real-time data refresh, connection timeout)  
**Constraints**: Bluetooth connectivity, vehicle-specific protocol compliance  
**Scale/Scope**: Single vehicle connection, multi-format reports, mobile-optimized UI

**User-provided Technical Details**:
- Client application uses Python to connect to Bluetooth endpoint of vehicle
- Explorations needed to verify required credentials and available data services
- Initial development environment deployment, then mobile phone availability
- Device targets: iPhone first, then Android
- Data visualization: latest alerts, fuel consumption stats, generic device stats (traveled km/miles), other reports
- Graphical widgets required: tables, histograms, effective visualization components

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Simplicity**:
- Projects: 3 (python-api, ios-app, android-app) - within limit
- Using framework directly? (TBD after research)
- Single data model? (vehicle diagnostic data model)
- Avoiding patterns? (TBD after research)

**Architecture**:
- EVERY feature as library? (diagnostic-client lib, reporting lib, mobile-interface lib)
- Libraries listed: [TBD after research]
- CLI per library: [TBD after research - diagnostic CLI, report CLI]
- Library docs: llms.txt format planned? Yes

**Testing (NON-NEGOTIABLE)**:
- RED-GREEN-Refactor cycle enforced? Yes
- Git commits show tests before implementation? Will enforce
- Order: Contract→Integration→E2E→Unit strictly followed? Yes
- Real dependencies used? Yes (actual Bluetooth, real mobile devices)
- Integration tests for: vehicle connection, data parsing, mobile display
- FORBIDDEN: Implementation before test, skipping RED phase

**Observability**:
- Structured logging included? Yes (connection status, data retrieval, errors)
- Frontend logs → backend? Yes (mobile app logs to Python API)
- Error context sufficient? Yes (Bluetooth errors, parsing errors, display errors)

**Versioning**:
- Version number assigned? 1.0.0
- BUILD increments on every change? Yes
- Breaking changes handled? Yes (vehicle protocol changes, mobile API changes)

## Project Structure

### Documentation (this feature)
```
specs/001-i-wanto-to/
├── plan.md              # This file (/plan command output)
├── research.md          # Phase 0 output (/plan command)
├── data-model.md        # Phase 1 output (/plan command)
├── quickstart.md        # Phase 1 output (/plan command)
├── contracts/           # Phase 1 output (/plan command)
└── tasks.md             # Phase 2 output (/tasks command - NOT created by /plan)
```

### Source Code (repository root)
```
# Option 3: Mobile + API (when "iOS/Android" detected)
api/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

ios/
└── [platform-specific structure]

android/
└── [platform-specific structure]
```

**Structure Decision**: Option 3 (Mobile + API) - Python API backend with iOS/Android mobile frontends

## Phase 0: Outline & Research
1. **Extract unknowns from Technical Context** above:
   - For each NEEDS CLARIFICATION → research task
   - For each dependency → best practices task
   - For each integration → patterns task

2. **Generate and dispatch research agents**:
   ```
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

3. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

**Output**: research.md with all NEEDS CLARIFICATION resolved

## Phase 1: Design & Contracts
*Prerequisites: research.md complete*

1. **Extract entities from feature spec** → `data-model.md`:
   - Entity name, fields, relationships
   - Validation rules from requirements
   - State transitions if applicable

2. **Generate API contracts** from functional requirements:
   - For each user action → endpoint
   - Use standard REST/GraphQL patterns
   - Output OpenAPI/GraphQL schema to `/contracts/`

3. **Generate contract tests** from contracts:
   - One test file per endpoint
   - Assert request/response schemas
   - Tests must fail (no implementation yet)

4. **Extract test scenarios** from user stories:
   - Each story → integration test scenario
   - Quickstart test = story validation steps

5. **Update agent file incrementally** (O(1) operation):
   - Run `/scripts/update-agent-context.sh [claude|gemini|copilot]` for your AI assistant
   - If exists: Add only NEW tech from current plan
   - Preserve manual additions between markers
   - Update recent changes (keep last 3)
   - Keep under 150 lines for token efficiency
   - Output to repository root

**Output**: data-model.md, /contracts/*, failing tests, quickstart.md, agent-specific file

## Phase 2: Task Planning Approach
*This section describes what the /tasks command will do - DO NOT execute during /plan*

**Task Generation Strategy**:
- Load `/templates/tasks-template.md` as base
- Generate tasks from Phase 1 design docs (contracts, data model, quickstart)
- Contract-driven development: Each API endpoint → contract test task [P]
- Entity-driven development: Each data model entity → model creation task [P] 
- User story validation: Each acceptance scenario → integration test task
- TDD implementation: Implementation tasks to make tests pass

**Specific Task Categories**:
1. **Contract Tests** (6-8 tasks): API endpoint validation for vehicles, sessions, data, reports, alerts
2. **Data Model Implementation** (5-6 tasks): SQLAlchemy models for Vehicle, DiagnosticSession, SystemData, Report, Alert, MobileDevice
3. **Integration Tests** (4-5 tasks): Bluetooth connection, OBD-II data collection, mobile app communication
4. **Core Services** (8-10 tasks): Vehicle registration, session management, data processing, report generation, alert system
5. **Mobile UI Components** (6-8 tasks): Dashboard, reports screen, alerts management, data visualization widgets
6. **End-to-End Workflows** (3-4 tasks): Complete diagnostic session, report generation, mobile sync

**Ordering Strategy**:
- **Phase 1**: Contract tests (must fail initially) - parallel execution [P]
- **Phase 2**: Data models and database schema - sequential for foreign key dependencies
- **Phase 3**: Integration tests for hardware - parallel execution [P] where possible
- **Phase 4**: Service layer implementation - dependency order (models → services → API)
- **Phase 5**: Mobile UI implementation - parallel execution [P] by screen/component
- **Phase 6**: End-to-end test implementation and validation

**Estimated Output**: 28-35 numbered, ordered tasks in tasks.md

**Task Prioritization**:
- Critical path: Vehicle registration → Session management → Data collection → Mobile display
- Parallel opportunities: Mobile UI components, API endpoints, data visualization widgets
- Dependencies: Hardware integration tests require real ELM327 adapter and test vehicle

**IMPORTANT**: This phase is executed by the /tasks command, NOT by /plan

## Phase 3+: Future Implementation
*These phases are beyond the scope of the /plan command*

**Phase 3**: Task execution (/tasks command creates tasks.md)  
**Phase 4**: Implementation (execute tasks.md following constitutional principles)  
**Phase 5**: Validation (run tests, execute quickstart.md, performance validation)

## Complexity Tracking
*Fill ONLY if Constitution Check has violations that must be justified*

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |

## Progress Tracking
*This checklist is updated during execution flow*

**Phase Status**:
- [x] Phase 0: Research complete (/plan command)
- [x] Phase 1: Design complete (/plan command)
- [x] Phase 2: Task planning complete (/plan command - describe approach only)
- [ ] Phase 3: Tasks generated (/tasks command)
- [ ] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Gate Status**:
- [x] Initial Constitution Check: PASS
- [x] Post-Design Constitution Check: PASS
- [x] All NEEDS CLARIFICATION resolved
- [ ] Complexity deviations documented

---
*Based on Constitution v2.1.1 - See `/memory/constitution.md`*