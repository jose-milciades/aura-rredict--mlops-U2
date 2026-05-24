from pathlib import Path
import csv
import tempfile
import unittest

import app


class PredictionModelTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_predictions_file = app.PREDICTIONS_FILE
        app.PREDICTIONS_FILE = Path(self.temp_dir.name) / "predictions.csv"

    def tearDown(self):
        app.PREDICTIONS_FILE = self.original_predictions_file
        self.temp_dir.cleanup()

    def test_young_patient_with_mild_respiratory_and_neurological_input_is_mild(self):
        prediction = app.predict_mock(
            [
                "paciente 20 anos",
                "tos leve",
                "congestion nasal",
                "condicion neurologica",
            ],
            "leve",
        )

        self.assertEqual(prediction["estado"], "ENFERMEDAD LEVE")

    def test_statistics_cycle_starts_empty_and_records_latest_prediction(self):
        initial_report = app.build_prediction_report()

        self.assertEqual(initial_report["total_predicciones"], 0)
        self.assertEqual(initial_report["ultimas_5_predicciones"], [])
        self.assertIsNone(initial_report["fecha_ultima_prediccion"])
        self.assertTrue(
            all(total == 0 for total in initial_report["predicciones_por_categoria"].values())
        )

        prediction = app.predict_mock(["fiebre", "tos", "dolor"], "terminal")
        app.record_prediction("terminal", prediction)

        updated_report = app.build_prediction_report()
        self.assertEqual(updated_report["total_predicciones"], 1)
        self.assertEqual(
            updated_report["predicciones_por_categoria"]["ENFERMEDAD TERMINAL"],
            1,
        )
        self.assertEqual(
            updated_report["ultimas_5_predicciones"][0]["estado_predicho"],
            "ENFERMEDAD TERMINAL",
        )
        self.assertEqual(
            updated_report["ultimas_5_predicciones"][0]["criticidad_predicha"],
            "terminal",
        )
        self.assertIsNotNone(updated_report["fecha_ultima_prediccion"])

        with app.PREDICTIONS_FILE.open(newline="", encoding="utf-8") as file:
            rows = list(csv.DictReader(file))

        self.assertEqual(rows[-1]["estado_predicho"], "ENFERMEDAD TERMINAL")
        self.assertEqual(rows[-1]["criticidad_entrada"], "terminal")

    def test_multiple_input_combinations_cover_all_five_categories(self):
        cases = [
            (["control sano", "sin fiebre", "sin dolor"], "sano", "NO ENFERMO"),
            (["tos leve", "congestion nasal", "dolor leve"], "leve", "ENFERMEDAD LEVE"),
            (["fiebre alta", "tos", "dolor toracico"], "aguda", "ENFERMEDAD AGUDA"),
            (
                ["fatiga persistente", "dolor cronico", "antecedente familiar"],
                "cronica",
                "ENFERMEDAD CRÓNICA",
            ),
            (
                ["deterioro rapido", "dolor intenso", "falla organica"],
                "terminal",
                "ENFERMEDAD TERMINAL",
            ),
        ]

        predicted_categories = {
            app.predict_mock(symptoms, severity)["estado"]
            for symptoms, severity, _expected_state in cases
        }

        self.assertEqual(
            predicted_categories,
            {
                "NO ENFERMO",
                "ENFERMEDAD LEVE",
                "ENFERMEDAD AGUDA",
                "ENFERMEDAD CRÓNICA",
                "ENFERMEDAD TERMINAL",
            },
        )
