"""
security-api
------------
Backend de ejemplo que reproduce, a propósito, el anti-patrón de
autenticación mediante una API key estática enviada en el header
'x-api-key'. Fines exclusivamente educativos.
"""

import os
from functools import wraps
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # permite que el frontend (servido desde otro origen) pueda llamar a esta API

# --------------------------------------------------------------------
# ANTI-PATRÓN: la "autenticación" es solo comparar un string estático.
# En un caso real, esto NUNCA debería vivir hardcodeado en el código,
# pero incluso leyéndola de una variable de entorno el patrón sigue
# siendo débil: una sola key compartida, sin expiración, sin owner,
# sin scopes, visible en el cliente (frontend) si alguien inspecciona
# las peticiones de red o el código fuente de app.js.
# --------------------------------------------------------------------
API_KEY = os.environ.get("API_KEY", "supersecret-123")


def require_api_key(f):
    """Decorador que implementa el anti-patrón: compara el header contra un valor fijo."""
    @wraps(f)
    def decorated(*args, **kwargs):
        provided_key = request.headers.get("x-api-key")

        if provided_key is None:
            return jsonify({"error": "Missing x-api-key header"}), 401

        if provided_key != API_KEY:
            return jsonify({"error": "Invalid API key"}), 401

        return f(*args, **kwargs)
    return decorated


# --------------------------------------------------------------------
# Endpoint público
# --------------------------------------------------------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


# --------------------------------------------------------------------
# Endpoint protegido - GET
# --------------------------------------------------------------------
@app.route("/api/data", methods=["GET"])
@require_api_key
def get_data():
    return jsonify({
        "message": "Protected data",
        "course": "Security Exercise",
        "status": "success"
    }), 200


# --------------------------------------------------------------------
# Endpoint protegido - POST
# --------------------------------------------------------------------
@app.route("/api/data", methods=["POST"])
@require_api_key
def post_data():
    # El body se ignora a propósito para este ejercicio
    return jsonify({"message": "POST received"}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
