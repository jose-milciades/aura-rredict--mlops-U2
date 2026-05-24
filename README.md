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

## Estructura del repositorio

```text
.
├── app.py              # Servidor HTTP, endpoints y logica mock de prediccion
├── Dockerfile          # Definicion de la imagen Docker del servicio
├── README.md           # Documentacion del proyecto
├── static/
│   ├── index.html      # Interfaz web para consultar el servicio
│   └── styles.css      # Estilos de la interfaz
└── .dockerignore       # Archivos excluidos del build Docker
```

## Endpoints

- `GET /`: interfaz web para ingresar sintomas y criticidad.
- `GET /health`: verificacion del estado del servicio.
- `POST /api/predict`: endpoint REST para obtener una prediccion simulada.

Ejemplo de consumo:

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

## Ejecucion con Docker

Construir la imagen:

```bash
docker build -t mock-ml-clinico:1.0 .
```

Ejecutar el contenedor:

```bash
docker run --rm -p 8000:8000 mock-ml-clinico:1.0
```

Abrir la aplicacion en:

```text
http://localhost:8000
```

## Notas

- El servicio usa solo librerias estandar de Python.
- La imagen base es `python:3.12-slim`.
- La prediccion es simulada; no debe usarse para diagnostico medico real.
- El proyecto esta pensado como base academica para practicar conceptos de MLOps, contenerizacion y exposicion de servicios de inferencia.
