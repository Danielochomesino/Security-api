"""
security-api (versión Docker)
------------------------------
Misma API que la versión anterior, pero ahora la API key ya NO vive
hardcodeada en el código. Se obtiene exclusivamente de la variable de
entorno API_KEY, que a su vez viene del archivo .env a través de
docker-compose. Si la variable no está definida, el servicio no
arranca: preferimos fallar rápido a arrancar con una key por defecto
insegura.
"""

import os
import sys
from functools import wraps
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --------------------------------------------------------------------
# La línea "API_KEY = os.environ.get('API_KEY', 'supersecret-123')"
# de la versión anterior queda ELIMINADA a propósito: ya no hay
# fallback hardcodeado. La key SOLO puede venir de la variable de
# entorno, que a su vez viene del .env vía docker-compose.
# --------------------------------------------------------------------
API_KEY = os.environ.get("API_KEY")

if not API_KEY:
    sys.exit("ERROR: la variable de entorno API_KEY no está definida. "
             "Revisa tu archivo .env y docker-compose.yml.")


def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        provided_key = request.headers.get("x-api-key")

        if provided_key is None:
            return jsonify({"error": "Missing x-api-key header"}), 401

        if provided_key != API_KEY:
            return jsonify({"error": "Invalid API key"}), 401

        return f(*args, **kwargs)
    return decorated


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/api/data", methods=["GET"])
@require_api_key
def get_data():
    return jsonify({
        "message": "Protected data",
        "course": "Security Exercise",
        "status": "success"
    }), 200


@app.route("/api/data", methods=["POST"])
@require_api_key
def post_data():
    return jsonify({"message": "POST received"}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
