FROM node:20-alpine AS base

WORKDIR /app

COPY package.json pnpm-workspace.yaml ./
COPY apps/passenger-web/package.json ./apps/passenger-web/

RUN npm install -g pnpm && pnpm install --filter passenger-web...

COPY . .

EXPOSE 3000

CMD ["pnpm", "--filter", "passenger-web", "dev"]
