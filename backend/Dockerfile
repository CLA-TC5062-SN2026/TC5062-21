FROM python:3.12-slim
WORKDIR /srv
COPY backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt
COPY backend/app backend/app
COPY backend/scripts backend/scripts
COPY S05_S06_A1/openapi_equipo.yaml S05_S06_A1/openapi_equipo.yaml
RUN useradd --create-home api
USER api
EXPOSE 8000
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
