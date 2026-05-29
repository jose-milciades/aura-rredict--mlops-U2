flowchart TD
    %% Definición de estilos para las capas
    classDef capa1 fill:#e3f2fd,stroke:#1e88e5,stroke-width:2px,color:#000;
    classDef capa2 fill:#f3e5f5,stroke:#8e24aa,stroke-width:2px,color:#000;
    classDef capa3 fill:#e8f5e9,stroke:#43a047,stroke-width:2px,color:#000;
    classDef capa4 fill:#fff3e0,stroke:#fb8c00,stroke-width:2px,color:#000;

    %% CAPA 1
    subgraph Capa_1 ["Capa 1: Infraestructura de Datos"]
        direction TB
        A1(Apache Airflow<br>Orquestador)
        A2[(Google BigQuery<br>Data Warehouse - Bronze/Silver)]
        A3(Apache Spark<br>Procesamiento y Limpieza)
        A4[(Feast<br>Feature Store - Capa Gold)]

        A1 -->|Programa extracción HCE| A2
        A2 <-->|Lee datos crudos / Guarda limpios| A3
        A3 -->|Calcula variables médicas| A4
    end
    class Capa_1 capa1

    %% CAPA 2
    subgraph Capa_2 ["Capa 2: Desarrollo DS y Experimentación"]
        direction TB
        B1(JupyterLab<br>Entorno de Trabajo)
        B2(Scikit-Learn + XGBoost<br>Modelado e imbalanced-learn SMOTE)
        B3[(MLflow<br>ML Metadata Store / Registry)]
        B4(Streamlit<br>App Human-in-the-Loop)

        A4 -.->|Extrae features offline| B1
        B1 -->|Programa scripts| B2
        B2 -->|Registra métricas y binarios| B3
        B3 -.->|Carga el mejor modelo| B4
        B4 -.->|Médico corrige / Etiqueta| A2
    end
    class Capa_2 capa2

    %% CAPA 3
    subgraph Capa_3 ["Capa 3: Pipelines Automatizados (CI/CD/CT)"]
        direction TB
        C1(Git / GitHub<br>Repositorio de Código)
        C2(GitHub Actions<br>Orquestador CI/CD)
        C3(Docker<br>Contenerización)
        C4[(Google Container Registry<br>Almacén de Imágenes)]

        B1 -.->|Push de código| C1
        C1 -->|Dispara tests| C2
        B3 -.->|Valida calidad del modelo| C2
        A1 -.->|Señal de CT por nuevos datos| C2
        C2 -->|Empaqueta si todo pasa| C3
        C3 -->|Guarda imagen inmutable| C4
    end
    class Capa_3 capa3

    %% CAPA 4
    subgraph Capa_4 ["Capa 4: Operaciones ML y Monitoreo"]
        direction TB
        D1(Google Cloud Run<br>Despliegue Serverless)
        D2(FastAPI<br>API Inferencia REST)
        D3(Evidently AI<br>Vigilancia Concept/Data Drift)
        D4(Grafana<br>Dashboards en vivo)

        C4 -.->|Pull de imagen a Producción| D1
        D1 --- D2
        A4 -.->|Extrae features online| D2
        D2 -->|Guarda historial de inferencias| A2
        A2 -.->|Lote nocturno de revisión| D3
        D3 -->|Envía métricas| D4
        D3 -.->|Alerta de degradación| A1
    end
    class Capa_4 capa4
