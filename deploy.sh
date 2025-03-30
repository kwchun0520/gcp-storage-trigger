#!/usr/bin/env bash
set -x
export $(cat .env | xargs)
poetry export -f requirements.txt --output requirements.txt --without-hashes
gcloud functions deploy gcs-trigger \
  --gen2 \
  --memory 128MiB \
  --trigger-event google.storage.object.finalize \
  --trigger-resource $1 \
  --entry-point=main \
  --runtime python39 \
  --region us-central1 