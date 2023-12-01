#!/bin/bash

set -a
source .env
set +a

gcloud run deploy $GCP_SERVICE_NAME \
  --image="eu.gcr.io/${GCP_PROJECT_ID}/${GCP_SERVICE_NAME}" \
  --region="${GCP_LOCATION}" \
  --platform=managed \
  --set-env-vars="$(awk -v ORS=, '{print $1}' .env | sed 's/,$//')"
