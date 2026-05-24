# Servicio Mock de Modelo MLOps Clínico

Esta solución implementa un servicio web REST y una página web sencilla para simular la respuesta de un modelo de machine learning clínico. No entrena un modelo real; usa una función mock que recibe síntomas y una criticidad indicada por el médico.

## Respuestas del modelo

La función puede retornar estos estados:

- `NO ENFERMO`
- `ENFERMEDAD LEVE`
- `ENFERMEDAD AGUDA`
- `ENFERMEDAD CRÓNICA`

## Construir la imagen Docker

Desde esta carpeta:

```bash
docker build -t mock-ml-clinico:1.0 .
```

## Ejecutar el contenedor

```bash
docker run --rm -p 8000:8000 mock-ml-clinico:1.0
```

El contenedor usa Linux mediante la imagen base `python:3.12-slim`.

## Usar la página web

Abra en el navegador:

```text
http://localhost:8000
```

Ingrese al menos tres síntomas y seleccione la criticidad: `sano`, `leve`, `aguda` o `cronica`.

## Consumir el servicio REST

Endpoint:

```text
POST /api/predict
```

Ejemplo:

```bash
curl -X POST http://localhost:8000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"severity":"aguda","symptoms":["fiebre","tos","dolor toracico"]}'
```

Respuesta esperada:

```json
{
  "estado": "ENFERMEDAD AGUDA",
  "criticidad": "aguda",
  "sintomas_evaluados": ["fiebre", "tos", "dolor toracico"],
  "confianza": 0.88,
  "mensaje": "Se recomienda priorizar valoracion clinica y descartar signos de alarma."
}
```

## Endpoints disponibles

- `GET /`: página web para el médico.
- `GET /health`: verificación de estado del servicio.
- `POST /api/predict`: predicción simulada del modelo.
