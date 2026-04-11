FROM node:20-alpine AS frontend-build
WORKDIR /workspace/frontend-admin
COPY frontend-admin/package*.json ./
RUN npm ci
COPY frontend-admin/ ./
RUN npm run build

FROM python:3.11-slim AS runtime
WORKDIR /workspace

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY backend/requirements.txt /workspace/backend/requirements.txt
RUN pip install --no-cache-dir -r /workspace/backend/requirements.txt

COPY backend/ /workspace/backend/

RUN rm -rf /workspace/backend/app/static
COPY --from=frontend-build /workspace/frontend-admin/dist /workspace/backend/app/static

RUN mkdir -p /workspace/data /workspace/storage/source/excel

ENV MEDIA_ROOT=/workspace/storage/source \
    EXCEL_ROOT=/workspace/storage/source/excel

EXPOSE 8000

WORKDIR /workspace/backend
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
