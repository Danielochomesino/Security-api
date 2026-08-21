# security-api

Backend de ejemplo que implementa (a propósito) un **anti-patrón de
autenticación**: proteger endpoints comparando el header `x-api-key`
contra un valor estático, sin JWT, sin expiración ni control por usuario.

Este proyecto es puramente educativo. **No usar este esquema de
autenticación en producción.**

## Endpoints

| Método | Ruta         | Requiere `x-api-key` | Descripción                 |
|--------|--------------|-----------------------|------------------------------|
| GET    | `/health`    | No                    | Estado del servicio          |
| GET    | `/api/data`  | Sí                    | Devuelve un JSON estático    |
| POST   | `/api/data`  | Sí                    | Devuelve mensaje de confirmación |

## Instalación

```bash
git clone <URL-de-este-repo>
cd security-api
python3 -m venv venv
source venv/bin/activate      # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Configuración

Copia `.env.example` a `.env` y ajusta la API key si quieres (opcional,
por defecto usa `supersecret-123`):

```bash
cp .env.example .env
```

Para que Flask lea el `.env` automáticamente en desarrollo, puedes
exportar la variable manualmente o usar `python-dotenv`. Para este
ejercicio, lo más simple es exportarla antes de correr el server:

```bash
export API_KEY=supersecret-123   # En Windows CMD: set API_KEY=supersecret-123
```

## Ejecución

```bash
python3 app.py
```

El servidor levanta en `http://localhost:5000`.

## Pruebas manuales con curl

```bash
# Test 1 — Health (sin key)
curl -i http://localhost:5000/health

# Test 2 — GET sin key -> 401
curl -i http://localhost:5000/api/data

# Test 3 — GET con key incorrecta -> 401
curl -i http://localhost:5000/api/data -H "x-api-key: wrong-key"

# Test 4 — GET con key correcta -> 200
curl -i http://localhost:5000/api/data -H "x-api-key: supersecret-123"

# Test 5 — POST sin key -> 401
curl -i -X POST http://localhost:5000/api/data

# Test 6 — POST con key correcta -> 200
curl -i -X POST http://localhost:5000/api/data -H "x-api-key: supersecret-123"
```

## Pruebas automatizadas

```bash
python3 -m pytest test_app.py -v
```

Debe mostrar 7/7 tests en verde.

## Nota de seguridad (anti-patrón)

Este proyecto expone intencionalmente las debilidades de usar una
API key estática como único mecanismo de autenticación:

- La key es la misma para todos los clientes (no hay identidad por usuario).
- No expira ni se puede revocar de forma granular.
- Si el frontend es una SPA, la key es visible inspeccionando el
  código fuente o las peticiones de red (DevTools → Network).
- No hay protección contra fuerza bruta ni logging de intentos fallidos.

Un esquema robusto usaría, por ejemplo, OAuth2 / JWT firmados con
expiración corta, refresh tokens, y validación server-side de scopes
por usuario.
