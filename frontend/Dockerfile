FROM node:20-alpine

WORKDIR /app

COPY package.json pnpm-lock.yaml* ./
RUN corepack enable && pnpm install --frozen-lockfile

# Source is mounted at runtime via docker-compose volumes for live reload.
# We deliberately skip `pnpm build` here — this image is for development only.
COPY . .

EXPOSE 3000
CMD ["pnpm", "dev"]
