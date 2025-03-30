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




  # gcloud run deploy gcs-trigger \
  #   --base-image python:3.9 \
  #   --platform managed \
  #   --source . \
  #   --region us-central1 \
  #   --cpu 1 \
  #   --memory 256Mi \
  #   --set-env-vars 'ENV=prod, VAR=1' \
  #   # --env-vars-file 'deployment/app.yaml'



  # gcloud eventarc triggers create TRIGGER_NAME  \
  #   --location=${REGION} \
  #   --destination-run-service=helloworld-events  \
  #   --destination-run-region=${REGION} \
  #   --event-filters="type=google.cloud.storage.object.v1.finalized" \
  #   --event-filters="bucket=PROJECT_ID-bucket" \
  #   --service-account=PROJECT_NUMBER-compute@developer.gserviceaccount.com