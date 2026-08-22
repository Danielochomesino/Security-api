# Imagen base ligera de Python
FROM python:3.12-slim

WORKDIR /app

# Copiamos primero solo requirements para aprovechar cache de Docker:
# si el código cambia pero las dependencias no, no se reinstalan.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Ahora copiamos el resto del código
COPY app.py .

EXPOSE 5000

# gunicorn como servidor de producción en vez del server de desarrollo de Flask
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
