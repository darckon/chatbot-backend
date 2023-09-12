from flask_restx import Namespace


class MSAssistant:
    api = Namespace(
        "api/v1/assistant-ms",
        description="Endpoints Disponibles para Assistant")
