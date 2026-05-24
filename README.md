# Servicio Mock para Prediccion de Enfermedades Huerfanas

Este repositorio contiene un servicio web mock que simula la respuesta de un modelo predictivo de inteligencia artificial para apoyar la identificacion temprana de enfermedades huerfanas a partir de sintomas reportados por un paciente.

## Autor

Jose Milciades Ordoñez Argote

## Problema

Las enfermedades huerfanas o raras suelen ser dificiles de diagnosticar porque tienen baja prevalencia, sintomas variados y, en muchos casos, se confunden con enfermedades mas comunes. Esto puede retrasar la atencion oportuna del paciente.

En un contexto clinico, contar con un modelo predictivo de IA puede ayudar a los medicos a priorizar casos, analizar combinaciones de sintomas y generar una alerta preliminar sobre el posible nivel de criticidad. Este proyecto no implementa un modelo real, sino un servicio simulado para practicar el despliegue, consumo y empaquetado de un componente de inferencia dentro de un flujo MLOps.

## Proposito

El objetivo del proyecto es exponer un servicio REST y una interfaz web sencilla que permitan enviar sintomas y recibir una respuesta simulada con:

- Estado estimado del paciente.
- Criticidad de la posible condicion.
- Sintomas evaluados.
- Nivel de confianza simulado.
- Mensaje de recomendacion clinica general.

La logica actual es deterministica y se encuentra en `app.py`. Sirve como base para reemplazar posteriormente el mock por un modelo entrenado real.

Actualmente el mock puede retornar cinco categorias:

- `NO ENFERMO`
- `ENFERMEDAD LEVE`
- `ENFERMEDAD AGUDA`
- `ENFERMEDAD CRÓNICA`
- `ENFERMEDAD TERMINAL`

## Estructura del repositorio

```text
.
├── app.py              # Servidor HTTP, endpoints y logica mock de prediccion
├── docker-compose.yml  # Ejecucion con volumen externo para el historico CSV
├── Dockerfile          # Definicion de la imagen Docker del servicio
├── README.md           # Documentacion del proyecto
├── static/
│   ├── index.html      # Interfaz web para consultar el servicio
│   └── styles.css      # Estilos de la interfaz
├── .dockerignore       # Archivos excluidos del build Docker
└── data/               # Carpeta local ignorada para almacenar predicciones CSV
```

## Endpoints

- `GET /`: interfaz web para ingresar sintomas y criticidad.
- `GET /health`: verificacion del estado del servicio.
- `GET /api/report`: reporte con conteos por categoria, ultimas 5 predicciones y fecha de la ultima prediccion.
- `GET /api/predictions.csv`: descarga del archivo CSV con el historico de predicciones.
- `POST /api/predict`: endpoint REST para obtener una prediccion simulada.

Ejemplo de consumo:

```bash
curl -X POST http://localhost:8000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"severity":"terminal","symptoms":["fiebre","tos","dolor toracico"]}'
```

Respuesta esperada:

```json
{
  "estado": "ENFERMEDAD TERMINAL",
  "criticidad": "terminal",
  "sintomas_evaluados": ["fiebre", "tos", "dolor toracico"],
  "confianza": 0.94,
  "mensaje": "Se recomienda atencion prioritaria, confirmacion diagnostica y manejo integral del paciente."
}
```

## Ejecucion con Docker

Construir la imagen:

```bash
docker build -t mock-ml-clinico:1.0 .
```

Ejecutar el contenedor:

```bash
docker run --rm -p 8000:8000 mock-ml-clinico:1.0
```

Ejecutar el contenedor con un volumen externo para conservar el historico CSV:

```bash
docker volume create mock-ml-predictions
docker run --rm -p 8000:8000 \
  -v mock-ml-predictions:/app/data \
  mock-ml-clinico:1.0
```

Tambien puede ejecutarse con Docker Compose:

```bash
docker volume create mock-ml-predictions
docker compose up --build
```

Abrir la aplicacion en:

```text
http://localhost:8000
```

## CI/CD

El repositorio incluye un pipeline de GitHub Actions en `.github/workflows/ci-cd.yml` con dos eventos principales:

- `pull_request` hacia `main`: comenta en el PR el inicio del pipeline y ejecuta validaciones del servicio.
- `push` en `main`: ejecuta las validaciones del servicio para cada commit integrado en la rama principal.

Las validaciones actuales compilan `app.py`, prueban la logica mock y construyen la imagen Docker.

## Notas

- El servicio usa solo librerias estandar de Python.
- La imagen base es `python:3.12-slim`.
- Cada prediccion exitosa se guarda en `/app/data/predictions.csv`.
- La prediccion es simulada; no debe usarse para diagnostico medico real.
- El proyecto esta pensado como base academica para practicar conceptos de MLOps, contenerizacion y exposicion de servicios de inferencia.
