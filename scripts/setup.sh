#!/usr/bin/env bash
set -e

echo "🚌 Setting up TransitPulse AI Workspace..."

pnpm install
cp -n .env.example .env || true
cp -n services/api/.env.example services/api/.env || true

echo "✅ Setup complete!"
