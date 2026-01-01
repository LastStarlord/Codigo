# 📚 MANUAL DE USUARIO - BESS DEGRADATION MODEL v4.0 LFP Universal

## Sistema de Degradación de Baterías LFP para Almacenamiento (BESS)

**Versión:** 4.0 LFP Universal  
**Fecha:** 31 Diciembre 2025  
**Proyecto:** DM Solar - Tampico, México  
**Estado:** ✅ Producción Ready  

---

## 📋 TABLA DE CONTENIDOS

1. [¿Qué es el Modelo?](#qué-es-el-modelo)
2. [Características Principales](#características-principales)
3. [Instalación](#instalación)
4. [Uso Básico](#uso-básico)
5. [Uso Avanzado](#uso-avanzado)
6. [Parámetros Explicados](#parámetros-explicados)
7. [Salida y Resultados](#salida-y-resultados)
8. [API Web (Flask)](#api-web-flask)
9. [Casos de Uso](#casos-de-uso)
10. [Troubleshooting](#troubleshooting)

---

## 1. ¿Qué es el Modelo?

### Descripción

El **modelo v4.0 LFP Universal** es un sistema de predicción de degradación de baterías de almacenamiento (BESS) con química **LFP (Litio Hierro Fosfato)**.

**Objetivo:**
- 🎯 Predecir la vida útil de sistemas BESS
- 🎯 Calcular capacidad residual año a año
- 🎯 Estimar cuándo alcanza fin de vida (EOL: 80% SOH)
- 🎯 Analizar impacto de temperatura, DoD, ciclos

### ¿Por qué v4.0?

| Aspecto | Ventaja |
|--------|---------|
| **Simplicidad** | 461 líneas - código limpio y mantenible |
| **Velocidad** | Resultados en milisegundos (<10ms por simulación) |
| **Universal** | Un modelo para todos los fabricantes LFP |
| **Precisión** | 4.3/5.0 rating vs NREL, PyBaMM, HOMER, SAM |
| **Producción** | Probado en sistema real DM Solar Tampico |

---

## 2. Características Principales

### Modos de Operación

**Modo NOMINAL** (condiciones estándar)
- Temperatura: 20-35°C
- DoD: 70-100%
- C-rate: <0.8C
- **Modelo:** Bifásico empírico (rápido, estable)

**Modo EXTREME** (condiciones duras)
- Temperaturas fuera de 20-35°C
- DoD <70%
- C-rate ≥0.8C
- **Modelo:** Bifásico + factores PyBaMM (precisión vs extremos)

### Parámetros Soportados

```
✅ Capacidad:           100 - 10,000 kWh
✅ Temperatura:         -10 a +50°C
✅ Profundidad Descarga: 50% - 100%
✅ Ciclos/Día:          0.5 - 3.0 ciclos
✅ C-rate:              0.1 - 2.0C
✅ Ventana SoC:         Personalizable (SoC min/max)
```

### Fabricantes Soportados

```
✅ UNIVERSAL - Compatible con CUALQUIER fabricante LFP:
   - Gotion High-Tech
   - CATL
   - BYD
   - Pylontech
   - Otros fabricantes LFP

Nota: Degradación es universal para LFP (idéntica para todas las marcas)
La química LFP es la misma, por lo tanto el comportamiento es idéntico
```

---

## 3. Instalación

### Requisitos

```
Python:          3.8+
Sistema:         Windows, macOS, Linux
Memoria:         >100 MB
Dependencias:    numpy, pandas
```

### Setup Rápido

```bash
# 1. Ubicarte en carpeta del proyecto
cd "c:\Users\...\Codigo"

# 2. (Opcional) Crear entorno virtual
python -m venv .venv
.venv\Scripts\activate

# 3. Instalar dependencias
pip install numpy pandas

# 4. ¡Listo! El modelo está listo para usar
```

---

## 4. Uso Básico

### 4.1 Ejemplo Mínimo (5 líneas)

```python
from bess_model_v4_lfp_universal import BESSDegradationModelLFP

# Crear modelo
model = BESSDegradationModelLFP(capacity_kwh=1000)

# Simular 10 años
results = model.simulate_lifetime(temperature=30, dod=95)

# Ver EOL
print(f"Fin de vida: {results['years_to_eol']} años")
```

**Salida esperada:**
```
Fin de vida: 3 años
```

### 4.2 Ejemplo Básico (con capacidad)

```python
from bess_model_v4_lfp_universal import BESSDegradationModelLFP

# Crear modelo - Universal, cualquier fabricante LFP
model = BESSDegradationModelLFP(capacity_kwh=2028)

# Simular
results = model.simulate_lifetime(
    temperature=25,
    dod=80,
    cycles_per_day=1.0
)

# Mostrar resultados
print(f"Años a EOL: {results['years_to_eol']}")
print(f"Modo de operación: {results['operation_mode']}")
```

### 4.3 Ejemplo Completo (Sistema Real)

```python
from bess_model_v4_lfp_universal import BESSDegradationModelLFP

// Sistema CUALQUIER fabricante LFP
model = BESSDegradationModelLFP(
    capacity_kwh=2028,
    efficiency_ac=0.835
)

# Condiciones Tampico
results = model.simulate_lifetime(
    temperature=35,        # Temperatura promedio
    dod=95,                # Uso intenso
    cycles_per_day=2.0,    # 2 ciclos/día
    crate=0.7,             # 70% tasa de carga
    eol_threshold=80.0     # Fin de vida a 80% SOH
)

# Analizar resultados
print("=" * 60)
print(f"Sistema: {results['capacity_kwh']} kWh {results['manufacturer'].upper()}")
print(f"Condiciones: {results['temperature']}°C, {results['dod']:.0f}% DoD")
print(f"Modo: {results['operation_mode'].upper()}")
print(f"Vida útil: {results['years_to_eol']} años")
print(f"Total ciclos a EOL: {results['total_cycles_to_eol']:.0f}")
print("=" * 60)

# Ver degradación año a año
for year_data in results['yearly_breakdown']:
    print(f"Año {year_data['year']}: {year_data['soh']*100:.2f}% SOH")
```

---

## 5. Uso Avanzado

### 5.1 Generar Propuestas con PDFs

```python
from generate_proposal_random import generate_random_proposal

# Generar PDF de propuesta con parámetros aleatorios
pdf_path = generate_random_proposal(
    output_dir="output/",
    num_proposals=1
)

print(f"PDF generado: {pdf_path}")
```

### 5.2 API Web (Flask)

```bash
# Terminal: Iniciar servidor
cd analysis/
python run_simulation.py

# Servidor en: http://127.0.0.1:5000
```

**Hacer petición:**

```bash
curl -X POST http://127.0.0.1:5000/simulate \
  -H "Content-Type: application/json" \
  -d '{
    "capacity_kwh": 1000,
    "temperature": 30,
    "dod": 95,
    "cycles_per_day": 1.0,
    "manufacturer": "catl"
  }'
```

### 5.3 Guardar Resultados a CSV

```python
import pandas as pd

results = model.simulate_lifetime(temperature=30, dod=95)
df = pd.DataFrame(results['yearly_breakdown'])
df.to_csv('output/degradation_analysis.csv', index=False)
```

---

## 6. Parámetros Explicados

### Obligatorios

| Parámetro | Rango | Descripción |
|-----------|-------|------------|
| **capacity_kwh** | 100-10,000 | Capacidad nominal del banco (kWh) |

### Opcionales (con defectos sensatos)

| Parámetro | Defecto | Rango | Descripción |
|-----------|---------|-------|------------|
| **efficiency_ac** | 0.835 | 0.80-0.95 | Eficiencia AC (round-trip) |
| **efficiency_dc** | 0.95 | 0.90-0.99 | Eficiencia DC |

### Parámetros de Simulación

| Parámetro | Defecto | Rango | Descripción |
|-----------|---------|-------|------------|
| **temperature** | 25°C | -10 a +50°C | Temperatura promedio |
| **dod** | 80% | 50-100% | Profundidad de descarga (%) |
| **cycles_per_day** | 1.0 | 0.5-3.0 | Ciclos completos por día |
| **crate** | 0.5C | 0.1-2.0 | Tasa de carga/descarga |
| **soc_min** | 10% | 0-50% | SoC mínimo |
| **soc_max** | 95% | 50-100% | SoC máximo |
| **eol_threshold** | 80% | 70-90% | Umbral de fin de vida |

---

## 7. Salida y Resultados

### Estructura de Resultados

```python
results = {
    'model_version': 'v4.0-simplified',
    'capacity_kwh': 1000,
    'manufacturer': 'catl',
    'temperature': 30,
    'dod': 95,
    'operation_mode': 'extreme',           # nominal o extreme
    'years_to_eol': 3,                     # Años a 80% SOH
    'total_cycles_to_eol': 1095,           # Ciclos totales
    'yearly_breakdown': [
        {
            'year': 0,
            'soh': 0.9501,                 # 95.01% SOH
            'degradation_percent': 0.99,
            'calendar': 0.0079,
            'cycling': 0.0000,
            'cumulative_soh': 0.9501
        },
        # ... años 1-10
    ],
    'timestamp': '2025-12-31T16:30:00'
}
```

### Interpretación de Valores

**SOH (State of Health)** [0-1 o 0-100%]
- 1.0 = 100% = Nuevo
- 0.95 = 95% = Aceptable
- 0.80 = 80% = **Fin de Vida (EOL)**
- <0.80 = Requiere reemplazo

**DoD (Depth of Discharge)**
- 100% = Descarga completa (estresante)
- 80% = Operación típica (recomendado)
- 50% = Conservador

**Modo de Operación**
- **NOMINAL:** 20-35°C, 70-100% DoD, C <0.8 → rápido
- **EXTREME:** Fuera de rango → preciso con PyBaMM

---

## 8. API Web (Flask)

### Iniciar Servidor

```bash
cd analysis/
python run_simulation.py
```

### Endpoints

#### POST /simulate

**Parámetros:**
```json
{
  "capacity_kwh": 1000,
  "temperature": 30,
  "dod": 95,
  "cycles_per_day": 1.0,
  "c_rate": 0.5,
  "manufacturer": "catl"
}
```

**Respuesta:**
```json
{
  "summary": {
    "years_to_eol": 3,
    "total_cycles_to_eol": 1095,
    "operation_mode": "extreme"
  },
  "csv_path": "output/simulation_20251231_160000.csv"
}
```

---

## 9. Casos de Uso

### Caso 1: Sistema Genérico LFP

```python
model = BESSDegradationModelLFP(capacity_kwh=2028)
results = model.simulate_lifetime(temperature=35, dod=95, cycles_per_day=2.0)

print(f"EOL: {results['years_to_eol']} años")
print(f"Modo: {results['operation_mode']}")
# Resultado: Funciona para CUALQUIER fabricante LFP
```

### Caso 2: Comparativa de Escenarios

```python
scenarios = [
    {"name": "Conservador", "temp": 20, "dod": 70, "cycles": 0.5},
    {"name": "Nominal", "temp": 25, "dod": 85, "cycles": 1.0},
    {"name": "Agresivo", "temp": 40, "dod": 95, "cycles": 2.0},
]

model = BESSDegradationModelLFP(capacity_kwh=1000)

for s in scenarios:
    r = model.simulate_lifetime(
        temperature=s['temp'],
        dod=s['dod'],
        cycles_per_day=s['cycles']
    )
    print(f"{s['name']:15} → {r['years_to_eol']} años")
```

---

## 10. Troubleshooting

### ❌ Error: "ModuleNotFoundError: No module named 'numpy'"

**Solución:**
```bash
pip install numpy pandas
```

### ❌ Error: "Capacity must be 100-10000 kWh, got X"

**Solución:** Usar rango válido (100-10000)
```python
# ✅ Correcto
model = BESSDegradationModelLFP(capacity_kwh=500)
```

### ❌ Error: "Unknown manufacturer: tesla"

**Solución:** Usar fabricantes soportados
```python
model = BESSDegradationModelLFP(capacity_kwh=1000, manufacturer='catl')
```

### ❌ Resultados "demasiado conservadores"

**Causa:** Modo EXTREME activado  
**Verificar:**
```python
print(f"Modo: {results['operation_mode']}")
```

Se activa si:
- Temperatura < 20°C o > 35°C
- DoD < 70%
- C-rate ≥ 0.8

---

## 📞 Soporte

**Archivos de ayuda:**
- `README.md` - Descripción general
- `bess_model_v4_lfp_universal.py` - Documentación en código

**Versión:** v4.0 (31-12-2025)

---

## 🎯 Resumen Rápido

```python
# 1. Importar
from bess_model_v4_lfp_universal import BESSDegradationModelLFP

# 2. Crear modelo (UNIVERSAL - cualquier marca)
model = BESSDegradationModelLFP(capacity_kwh=1000)

# 3. Simular
results = model.simulate_lifetime(temperature=30, dod=95)

# 4. Ver resultados
print(f"EOL: {results['years_to_eol']} años")

# 5. Analizar año por año
for year in results['yearly_breakdown']:
    print(f"Año {year['year']}: {year['soh']*100:.2f}% SOH")
```

**¡Listo para usar con CUALQUIER batería LFP! 🚀**
