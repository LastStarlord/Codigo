# Proyecto BESS - Modelo de Degradación v3.2 Universal LFP

Modelo de degradación universal para sistemas BESS con química LFP, compatible con múltiples fabricantes.

## 📋 Descripción

Sistema de modelado de degradación para baterías BESS con química LFP (Litio Hierro Fosfato). Completamente generalizado para funcionar con cualquier fabricante y especificaciones de sistema.

**Compatible con:**
- ✅ Gotion High-Tech (China)
- ✅ CATL / Contemporary Amperex Technology (China)
- ✅ BYD Co., Ltd. (China)
- ✅ Pylontech (Alemania/China)
- ✅ Y cualquier otro fabricante LFP

## 📁 Archivos Principales

### ⭐ RECOMENDADO: Usar `bess_model_v4_lfp_universal.py`

```python
from bess_model_v4_lfp_universal import BESSDegradationModelLFP
```

**Por qué este modelo:**
- ✅ Arquitectura simplificada (sin redundancia artificial)
- ✅ **Técnicamente correcto**: Reconoce que LFP es universal en todos los fabricantes
- ✅ Fácil de mantener (cambios en 1 lugar, no 4)
- ✅ Resultados idénticos al modelo v4.0 original
- ✅ API compatible (mismo nombre de clase, métodos, parámetros)

### Alternativa: `bess_degradation_model_v3.py` (Modelo Antiguo v3.2)

Aún funciona, pero mantiene redundancia antigua:
- ✅ API igual a v4.0 LFP Universal
- ❌ Código más complejo
- ❌ Mayor tamaño de archivo
- ⚠️ Mejor para referencia histórica

**Ver:** `COMPARACION_MODELO_v4.txt` para análisis completo de cambios.

## 🚀 Uso Rápido

### Usando Presets (Recomendado)
```python
from bess_degradation_model_v3 import BESSDegradationModelLFP

# Sistema Gotion
model = BESSDegradationModelLFP.from_preset(
    manufacturer="gotion",
    capacity_kwh=2028,
    power_kw=500,
    temp_celsius=30
)

# Sistema CATL
model = BESSDegradationModelLFP.from_preset(
    manufacturer="catl",
    capacity_kwh=500,
    power_kw=250,
    temp_celsius=25
)

# Simular vida útil
df, years_to_eol = model.simulate_lifetime(eol_threshold=0.80)
model.print_summary()
```

### Configuración Personalizada
```python
model = BESSDegradationModelLFP(
    capacity_kwh=500,          # 100-10,000 kWh
    power_kw=250,              # 50-5,000 kW
    temp_celsius=30,           # -10 a +50°C
    dod=0.95,                  # 0.5-1.0
    storage_days=180,          # días pre-operación
    ac_efficiency=0.85,        # 0.80-0.95
    cycles_per_day=1.0,        # 0.5-3.0
    custom_name="Mi Sistema LFP"
)
```

## 📊 Especificaciones del Proyecto Referencia (Gotion)

| Parámetro | Valor |
|-----------|-------|
| Capacidad DC | 2,028 kWh |
| Capacidad AC | 1,693 kWh |
| Potencia | 500 kW |
| Química | LFP (Litio Hierro Fosfato) |
| Temperatura Operación | 26-35°C |
| DoD | 95% |
| Ciclos/año | 365 (1/día) |
| EOL Target | 80% SOH |
| Vida útil | ~3 años a EOL |

## 📁 Estructura del Proyecto

```
Codigo/
├── bess_degradation_model_v3.py    ← MODELO PRINCIPAL (v3.2 Universal)
├── test_v32.py                     ← Tests de validación
├── README.md                       ← Este archivo
│
├── core/
│   ├── __init__.py
│   └── bess_model.py               ← Copia de v3.2
│
├── data/
│   ├── DM_SOLAR_TAMPICO.txt        ← Datos de referencia
│   ├── bess_degradation_v3.csv     ← Resultados simulación
│   └── lfp_manufacturer_1.csv      ← Datos fabricante
│
├── analysis/
│   ├── analisis_modelo_v3.py       ← Análisis detallado
│   ├── run_simulation.py           ← API Flask
│   └── test_*.py                   ← Tests
│
├── output/
│   ├── bess_analysis_v3.html       ← Visualización interactiva
│   ├── bess_degradation_v3.png     ← Gráficas
│   └── bess_lfp_universal_comparison.png
│
├── tools/                          ← Herramientas auxiliares
│
└── archive/                        ← Versiones obsoletas
```

## 🔬 Componentes del Modelo

### 1. Degradación Cíclica (Bifásica NO-lineal)
```
Fase 1 (0-3 años): D = 0.0545 × años × factor_DoD
Fase 2 (3+ años):  D = 16.35% + 0.38% × (años - 3)
```
- Simula envejecimiento acelerado inicial
- Estabilización en años posteriores
- Factor DoD normalizado a 95%

### 2. Degradación Calendárica (Tabla Universal LFP)
Basada en datos de múltiples fabricantes:

| Rango Temp. | Mes 1 | Mes 2-3 | Mes 10+ |
|-------------|-------|---------|---------|
| ≤15°C       | 0.79% | 0.27%   | 0.10%   |
| 16-25°C     | 1.23% | 0.41%   | 0.16%   |
| **26-35°C** | 1.87% | 0.63%   | 0.27%   |
| 36-45°C     | 2.75% | 0.93%   | 0.47%   |

### 3. Pre-degradación FAT-SAT
- Mes 1: Tasa acelerada según temperatura
- Meses 2+: Tasa reducida (~1/3 de mes 1)
- Típico: 180 días pre-operación

### 4. Combinación Total
```
D_total = 1 - (1 - D_cíclica) × (1 - D_calendárica)
```

## ✅ Validación de Parámetros

El modelo valida automáticamente:

| Parámetro | Rango Válido |
|-----------|-------------|
| Capacidad | 100 - 10,000 kWh |
| Potencia | 50 - 5,000 kW |
| Temperatura | -10 a +50°C |
| DoD | 0.5 - 1.0 |
| Eficiencia AC | 0.80 - 0.95 |
| Ciclos/día | 0.5 - 3.0 |

Lanza `ValueError` si están fuera de rango.

## 📈 Ejemplo de Salida

```
================================================================================
BESS DEGRADATION MODEL v3.2 - UNIVERSAL LFP
================================================================================
Sistema:                  Gotion High-Tech Co., Ltd. 2028 kWh
Fabricante:               Gotion High-Tech Co., Ltd.

CAPACIDAD:
  DC nominal:             2,028 kWh
  AC nominal:             1,693 kWh
  Potencia:               500 kW

OPERACION:
  Temperatura:            30°C (Rango: 26-35°C)
  Profundidad descarga:   95%
  Ciclos/día:             1.0
  Ciclos/año:             365
  Eficiencia AC:          83.5%

ALMACENAJE PRE-OPERACIONAL:
  Días FAT-SAT:           180 días
  Pre-degradación:        4.99%
  SOH post-almacenaje:    95.01%
================================================================================
```

## 🧪 Tests

Ejecutar tests de validación:
```bash
python test_v32.py
```

Salida esperada:
- ✓ TEST 1: Crear modelo con preset Gotion
- ✓ TEST 2: Crear modelo con preset CATL
- ✓ TEST 3: Crear modelo personalizado
- ✓ TEST 4: Validación de parámetros
- ✓ TEST 5: Simulación de vida útil

## 📦 Dependencias

```
numpy
pandas
matplotlib
```

Instalar:
```bash
pip install numpy pandas matplotlib
```

## 🔄 Cambios v3.0 → v3.2

| Aspecto | v3.0 | v3.2 |
|---------|------|------|
| **Clase** | BESSDegradationModel | BESSDegradationModelLFP |
| **Generalización** | Gotion específico | Universal (múltiples fabricantes) |
| **Presets** | No | Sí (4+ fabricantes) |
| **Validación** | Manual | Automática |
| **Rango Capacidad** | Fija | 100-10,000 kWh |
| **Rango Temperatura** | 26-35°C | -10 a +50°C |
| **Documentación** | Modelo específico | Universal |

## 📝 Notas de Diseño

1. **Universalidad**: Tabla de degradación calendárica es estándar para todas las baterías LFP
2. **Flexibilidad**: Parámetros completamente ajustables
3. **Validación**: Previene parámetros inválidos en tiempo de inicialización
4. **Reutilización**: Compatible con code existente mediante aliases
5. **Escalabilidad**: Puede usarse para sistemas 100 kWh hasta 10 MWh

## 📞 Soporte

Para preguntas o problemas:
- Revisar `test_v32.py` para ejemplos de uso
- Consultar `analysis/analisis_modelo_v3.py` para análisis detallado
- Ver `output/bess_analysis_v3.html` para visualización interactiva

---

**Fecha:** 31 Diciembre 2025  
**Versión:** 3.2 - Universal LFP  
**Estado:** ✅ Producción
