# AI Agent Instructions for BESS Degradation Model Codebase

## Project Overview

**BESS Degradation Model v3-4**: A universal LFP battery degradation simulator for energy storage systems. Compatible with multiple manufacturers (Gotion, CATL, BYD, Pylontech). Production-ready with 3 model versions (v3.2 empirical, v3.3 PyBaMM, v4.0 unified).

## Architecture & Component Boundaries

### Three-Model Strategy (Critical)
- **v3.2** (`bess_degradation_model_v3.py`): Bi-phasic empirical model - fast, stable in nominal conditions (20-35°C, DoD 70-100%, C-rate <0.8)
- **v3.3** (`bess_degradation_model_v33_pybamm.py`): PyBaMM integration - mechanistic precision for reference (archived, not actively used)
- **v4.0** (`bess_degradation_model_v4.py`): **PRODUCTION MODEL** - adaptive selector with **active PyBaMM**
  - **Nominal mode**: Uses v3.2 bifasic model (proven, stable) for standard conditions
  - **Extreme mode**: Applies PyBaMM factors (Arrhenius, SEI, C-rate, SoC window) for harsh conditions
  - Automatically routes based on: temperature, DoD, C-rate

**Mode Selection Logic**:
```python
# Nominal: 20-35°C AND 70-100% DoD AND C-rate < 0.8
# Extreme: Everything else (temperatures outside 20-35°C, DoD <70%, C-rate ≥0.8)
```

**PyBaMM Factors in v4.0**:
- **Arrhenius** (Ea=40 kJ/mol): Temperature-dependent degradation (1.75x at 15°C, 0.36x at 45°C)
- **SEI Growth** (parabolic): Solid Electrolyte Interphase formation with cycle count
- **C-rate Sensitivity** (exp=0.4): High-rate operation penalty (1.32x at 1.0C vs 0.5C baseline)
- **SoC Window**: Penalties for extreme operating ranges (1.73x for 0-100% window)
- **Impedance Growth**: Exponential resistance increase
- **Efficiency Factor**: Thermal stress from energy losses

### Data Layers
1. **Empirical Base**: Universal LFP calendric degradation tables (`CALENDAR_TABLE_LFP`, `PRESTORAGE_TABLE_LFP`) - temperature-binned, manufacturer-agnostic
2. **Bifasic Cycling Model** (v3.2/v4.0 nominal): 
   - Phase 1 (0-3 years): 5.45% per year (rapid SEI formation)
   - Phase 2 (3+ years): 0.38% per year (steady state)
3. **Mechanistic Factors** (v4.0 extreme): PyBaMM-based Arrhenius, SEI growth, C-rate sensitivity, SoC window effects
4. **Manufacturer Presets**: MANUFACTURER_PRESETS dict with specs for Gotion, CATL, BYD, Pylontech

### Service Boundaries
- **`core/bess_model.py`**: Identical copy of v3.2 - DO NOT modify independently; changes must sync to v3.2
- **`analysis/run_simulation.py`**: Flask API (POST `/simulate`) - lazy imports model, saves CSV output to `OUTPUT_DIR`
- **HTML Frontend** (`bess_simulator.html`): Client-side parameter input, calls Flask endpoint, displays summary metrics
- **Tools** (`tools/*.py`): PDF conversion utilities, OCR support - not core model logic

## Key Workflows

### Standard Simulation Flow
```python
# 1. Instantiate with presets (preferred)
model = BESSDegradationModelLFP.from_preset(
    manufacturer="gotion",
    capacity_kwh=2028,
    power_kw=500,
    temp_celsius=30
)

# 2. OR custom parameters (must validate within ranges)
model = BESSDegradationModelLFP(
    capacity_kwh=150,           # 100-10000 kWh
    power_kw=75,                # 50-5000 kW
    temp_celsius=40,            # -10 to +50°C
    dod=0.85,                   # 0.5-1.0
    cycles_per_day=1.0,         # 0.5-3.0
    ac_efficiency=0.835,        # 0.80-0.95
)

# 3. Run lifetime simulation (yields df + EOL year)
df_lifetime, years_to_eol = model.simulate_lifetime(eol_threshold=0.80)

# 4. Generate output (CSV auto-saved in Flask flow)
model.print_summary()
```

### Testing Protocol
- **`test_v32.py`**: Unit tests for v3.2 presets, custom configs, parameter validation
- **`test_pybamm_v33.py`**: v3.3 PyBaMM integration tests
- **`test_v4_comparison.py`**: v4.0 nominal vs extreme comparison
- **`test_v4_validation.py`**: Full v4.0 validation (matches v3.2 in nominal, applies PyBaMM in extreme)
- **`test_v4_pybamm.py`**: PyBaMM factor activation and effect validation
- **`compare_all_models.py`**: Generates comparison HTML report across versions
- Run tests BEFORE merging model changes: `python test_v*.py`

### Flask Deployment
```bash
cd analysis/
python run_simulation.py  # Serves on 127.0.0.1:5000
# POST /simulate with JSON params
# GET /download/<filename> returns CSV
```

## Critical Conventions & Patterns

### Parameter Validation
- **ALWAYS validate ranges** in `__init__`: capacity, power, temperature, DoD, efficiency, cycles_per_day
- Raise `ValueError` with clear message including valid range (see v3.2 implementation)
- Do NOT silently clip/coerce parameters

### Degradation Computation
- **Bi-phasic model** (v3.2/v4.0): Rapid initial fade (~1-2 years) then flat rate
  - Year 1 cycling: Heavy degradation from SEI formation
  - Year 2+: Linear calendar + cycle at steady state
- **Temperature sensitivity**: Degradation accelerates ~3x from 15°C to 45°C (embedded in CALENDAR_TABLE_LFP)
- **Output**: Annual SOH (state of health %) and residual capacity (kWh)

### Naming & Terminology
- Use Spanish/English mixed docs (reflect codebase style)
- Manufacturer names: lowercase keys ("gotion", "catl", "byd", "pylontech")
- Thermal zones: "≤15°C", "16-25°C", "26-35°C", "36-45°C"
- EOL definition: 80% SOH (state of health) is the hardcoded target

### File Organization
- Model implementations: root level (`bess_degradation_model_vX.py`)
- Tests: root level (`test_*.py`)
- Analysis/API: `analysis/` directory
- Utility tools: `tools/` directory
- Data files: `data/` directory (CSV, TXT)
- Output reports: `output/` directory (HTML, PNG)

## Integration Points & External Dependencies

### PyBaMM (v3.3 only)
- Used for mechanistic electrochemistry when available
- Graceful fallback to v3.2 if PyBaMM import fails
- Do NOT require PyBaMM for v3.2/v4.0 core functionality

### Flask Routes (v3.3+)
- Endpoint `/simulate` expects JSON with capacity_kwh, power_kw, temp_celsius, dod, cycles_per_day, c_rate, soc_min, soc_max, eol_threshold
- Always return JSON with `summary` dict + `csv_path` or `error` dict + traceback
- CSV output saves to `OUTPUT_DIR` (script directory)

### HTML Frontend
- Static file served from `analysis/` directory
- No database; all state in browser/request payload
- Uses fetch API (POST to `/simulate`, GET to `/download/`)

## Example: Adding a New Manufacturer Preset

```python
# In MANUFACTURER_PRESETS dict:
"new_brand": {
    "name": "New Brand Co., Ltd.",
    "chemistry": "LFP",
    "typical_cycle_life_90dod": 12000,  # From datasheet
    "warranty_years": 10,
    "ac_efficiency_typical": 0.85,
    "notes": "Standard LFP global / Regional notes"
}

# Then create model:
model = BESSDegradationModelLFP.from_preset(
    manufacturer="new_brand",
    capacity_kwh=500,
    power_kw=250,
    temp_celsius=30
)
```

## Common Pitfalls & Debugging

1. **Parameter out of range silently fails**: Always check `_validate_parameters()` output - logs to console before exception
2. **v3.2 and `core/bess_model.py` diverge**: They must stay in sync; changes to one require updating the other
3. **PyBaMM import missing**: v3.3 gracefully degrades; check if `pip install pybamm` is required for v3.3 tests
4. **CSV not saving in Flask**: Verify `OUTPUT_DIR` is writable and points to `analysis/` directory
5. **Temperature binning off**: Calendar table lookups are string-based ("26-35°C"); ensure temp ranges match keys exactly
6. **v4.0 not using PyBaMM**: Verify operation mode detection - check that temperature/DoD/C-rate trigger "extreme" mode correctly. PyBaMM only activates when outside nominal range (20-35°C, 70-100% DoD, C-rate <0.8)

## Files to Review for Context

- [bess_degradation_model_v3.py](bess_degradation_model_v3.py): Core v3.2 implementation (FOUNDATIONAL)
- [bess_degradation_model_v4.py](bess_degradation_model_v4.py): Production unified model with mechanistic factors
- [README.md](README.md): Quick start & project overview
- [MANUAL_USUARIO.md](MANUAL_USUARIO.md): Detailed user guide with all parameters explained
- [test_v32.py](test_v32.py): Reference for testing patterns
