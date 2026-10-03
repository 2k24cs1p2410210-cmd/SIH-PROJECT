FROM node:20-alpine AS base

WORKDIR /app

COPY package.json pnpm-workspace.yaml ./
COPY apps/admin-web/package.json ./apps/admin-web/

RUN npm install -g pnpm && pnpm install --filter admin-web...

COPY . .

EXPOSE 3001

CMD ["pnpm", "--filter", "admin-web", "dev"]
