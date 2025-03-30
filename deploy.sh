#!/usr/bin/env bash
set -x
export $(cat .env | xargs)
BUCEKT=$1
poetry export -f requirements.txt --output requirements.txt --without-hashes
gcloud functions deploy gcs-trigger \
  --gen2 \
  --memory=128MiB \
  --trigger-event-filters="type=google.cloud.storage.object.v1.finalized" \
  --trigger-event-filters="bucket=$BUCKET" \
  --entry-point=main \
  --runtime python39 \
  --region us-central1
