from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs
import json
import os


BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

STATUS_BY_SEVERITY = {
    "sano": "NO ENFERMO",
    "leve": "ENFERMEDAD LEVE",
    "aguda": "ENFERMEDAD AGUDA",
    "cronica": "ENFERMEDAD CRÓNICA",
}

ALIASES = {
    "no enfermo": "sano",
    "sin sintomas": "sano",
    "sintomas leves": "leve",
    "sintomas agudos": "aguda",
    "sintomas cronicos": "cronica",
    "cronico": "cronica",
    "crónica": "cronica",
    "crónico": "cronica",
}


def normalize_text(value):
    return str(value or "").strip().lower()


def predict_mock(symptoms, severity):
    clean_symptoms = [symptom.strip() for symptom in symptoms if symptom and symptom.strip()]
    normalized_severity = normalize_text(severity)
    normalized_severity = ALIASES.get(normalized_severity, normalized_severity)

    if len(clean_symptoms) < 3:
        raise ValueError("Debe ingresar al menos 3 sintomas.")

    if normalized_severity not in STATUS_BY_SEVERITY:
        raise ValueError(
            "La criticidad debe ser una de estas opciones: sano, leve, aguda o cronica."
        )

    return {
        "estado": STATUS_BY_SEVERITY[normalized_severity],
        "criticidad": normalized_severity,
        "sintomas_evaluados": clean_symptoms,
        "confianza": confidence_for(normalized_severity, clean_symptoms),
        "mensaje": message_for(normalized_severity),
    }


def confidence_for(severity, symptoms):
    base_confidence = {
        "sano": 0.96,
        "leve": 0.82,
        "aguda": 0.88,
        "cronica": 0.91,
    }[severity]
    symptom_bonus = min((len(symptoms) - 3) * 0.01, 0.04)
    return round(min(base_confidence + symptom_bonus, 0.99), 2)


def message_for(severity):
    messages = {
        "sano": "No se identifican senales de enfermedad en esta simulacion.",
        "leve": "Se recomienda seguimiento y manejo sintomatico segun criterio medico.",
        "aguda": "Se recomienda priorizar valoracion clinica y descartar signos de alarma.",
        "cronica": "Se recomienda seguimiento especializado y revision de antecedentes.",
    }
    return messages[severity]


class MockModelHandler(BaseHTTPRequestHandler):
    server_version = "MockModelService/1.0"

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self.send_static_file("index.html", "text/html; charset=utf-8")
            return

        if self.path == "/static/styles.css":
            self.send_static_file("styles.css", "text/css; charset=utf-8")
            return

        if self.path == "/health":
            self.send_json({"status": "ok", "service": "mock-ml-diagnosis"})
            return

        self.send_error(404, "Ruta no encontrada")

    def do_POST(self):
        if self.path != "/api/predict":
            self.send_error(404, "Ruta no encontrada")
            return

        try:
            payload = self.read_payload()
            symptoms = payload.get("symptoms", [])
            severity = payload.get("severity", "")

            if isinstance(symptoms, str):
                symptoms = [item.strip() for item in symptoms.split(",")]

            prediction = predict_mock(symptoms, severity)
            self.send_json(prediction)
        except ValueError as error:
            self.send_json({"error": str(error)}, status=400)
        except json.JSONDecodeError:
            self.send_json({"error": "El cuerpo de la peticion debe ser JSON valido."}, status=400)

    def read_payload(self):
        content_length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(content_length).decode("utf-8")

        content_type = self.headers.get("Content-Type", "")
        if "application/json" in content_type:
            return json.loads(raw_body or "{}")

        if "application/x-www-form-urlencoded" in content_type:
            form = parse_qs(raw_body)
            return {
                "severity": form.get("severity", [""])[0],
                "symptoms": [
                    form.get("symptom_1", [""])[0],
                    form.get("symptom_2", [""])[0],
                    form.get("symptom_3", [""])[0],
                    form.get("symptom_4", [""])[0],
                ],
            }

        return json.loads(raw_body or "{}")

    def send_static_file(self, filename, content_type):
        file_path = STATIC_DIR / filename
        if not file_path.exists():
            self.send_error(404, "Archivo no encontrado")
            return

        data = file_path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def send_json(self, payload, status=200):
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format_, *args):
        print("%s - - [%s] %s" % (self.address_string(), self.log_date_time_string(), format_ % args))


def run():
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    server = ThreadingHTTPServer((host, port), MockModelHandler)
    print(f"Mock ML service running on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
