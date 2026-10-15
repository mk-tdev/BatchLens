FROM node:24-alpine AS frontend
WORKDIR /build
COPY package.json package-lock.json tsconfig.json vite.config.ts ./
COPY frontend ./frontend
RUN npm ci && npm run build

FROM python:3.13-slim
WORKDIR /app
COPY requirements.lock ./
RUN pip install --no-cache-dir -r requirements.lock
COPY backend ./backend
COPY --from=frontend /build/dist ./dist
RUN useradd --create-home batchlens && chown -R batchlens:batchlens /app
USER batchlens
ENV STORAGE_BACKEND=firestore COOKIE_SECURE=true PORT=8080
EXPOSE 8080
CMD ["sh", "-c", "uvicorn backend.app.main:app --host 0.0.0.0 --port ${PORT}"]
