# Monorepo for understanding trades

## Structure

- backend: FastAPI service managed by uv
- frontend: Next.js app
- infra: Docker Compose and shared environment files
- shared: Cross-cutting schemas/types

## Quick start

```bash
cd infra
docker compose up --build
```
