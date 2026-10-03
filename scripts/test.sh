#!/usr/bin/env bash
set -e
pnpm test
cd services/api && pytest
