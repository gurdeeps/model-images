# syntax=docker/dockerfile:1.6
#
# Multi-stage build: downloads HF models per manifest, then ships only the
# /models tree on `FROM scratch`. Consume from another Dockerfile via:
#
#   COPY --from=ghcr.io/gurdeeps/model-images/sentiment:latest /models /opt/models
#
ARG MANIFEST

FROM python:3.11-slim AS builder
ARG MANIFEST
WORKDIR /work

RUN pip install --no-cache-dir "huggingface-hub>=0.23,<1.0"

COPY scripts/download_models.py ./
COPY ${MANIFEST} ./manifest.txt

# HF_TOKEN passed as build secret for gated/private models (no-op otherwise)
RUN --mount=type=secret,id=hf_token,required=false \
    HF_TOKEN="$(cat /run/secrets/hf_token 2>/dev/null || true)" \
    python download_models.py manifest.txt /models

FROM scratch
COPY --from=builder /models /models
