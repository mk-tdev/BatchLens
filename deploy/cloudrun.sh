#!/usr/bin/env bash
set -euo pipefail
# Run from the BatchLens source directory in authenticated Cloud Shell.
BATCHLENS_PROJECT="${BATCHLENS_PROJECT:-yourstorieslive-i18n}"
BATCHLENS_REGION="${BATCHLENS_REGION:-asia-southeast1}"
BATCHLENS_MODEL="${BATCHLENS_MODEL:-gemini-3.5-flash-lite}"
BATCHLENS_RUNTIME="batchlens-runtime@${BATCHLENS_PROJECT}.iam.gserviceaccount.com"
BATCHLENS_BUILDER="batchlens-builder@${BATCHLENS_PROJECT}.iam.gserviceaccount.com"
BATCHLENS_BUCKET="${BATCHLENS_PROJECT}-batchlens-builds"
BATCHLENS_IMAGE="${BATCHLENS_REGION}-docker.pkg.dev/${BATCHLENS_PROJECT}/batchlens/app:$(date -u +%Y%m%d%H%M%S)"
case "${1:-}" in
 setup)
  gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com aiplatform.googleapis.com firestore.googleapis.com iam.googleapis.com --project="$BATCHLENS_PROJECT" --quiet
  gcloud iam service-accounts describe "$BATCHLENS_RUNTIME" --project="$BATCHLENS_PROJECT" >/dev/null 2>&1 || gcloud iam service-accounts create batchlens-runtime --display-name="BatchLens runtime" --project="$BATCHLENS_PROJECT"
  gcloud iam service-accounts describe "$BATCHLENS_BUILDER" --project="$BATCHLENS_PROJECT" >/dev/null 2>&1 || gcloud iam service-accounts create batchlens-builder --display-name="BatchLens container builder" --project="$BATCHLENS_PROJECT"
  gcloud iam roles describe batchlensPredict --project="$BATCHLENS_PROJECT" >/dev/null 2>&1 || gcloud iam roles create batchlensPredict --project="$BATCHLENS_PROJECT" --title="BatchLens Gemini inference" --permissions=aiplatform.endpoints.predict,serviceusage.services.use --stage=GA
  gcloud projects add-iam-policy-binding "$BATCHLENS_PROJECT" --member="serviceAccount:$BATCHLENS_RUNTIME" --role="projects/$BATCHLENS_PROJECT/roles/batchlensPredict" --condition=None --quiet >/dev/null
  gcloud projects add-iam-policy-binding "$BATCHLENS_PROJECT" --member="serviceAccount:$BATCHLENS_RUNTIME" --role=roles/datastore.user --condition="expression=resource.name==\"projects/$BATCHLENS_PROJECT/databases/batchlens\",title=batchlens_database_only" --quiet >/dev/null
  gcloud projects add-iam-policy-binding "$BATCHLENS_PROJECT" --member="serviceAccount:$BATCHLENS_BUILDER" --role=roles/logging.logWriter --condition=None --quiet >/dev/null
  gcloud artifacts repositories describe batchlens --location="$BATCHLENS_REGION" --project="$BATCHLENS_PROJECT" >/dev/null 2>&1 || gcloud artifacts repositories create batchlens --repository-format=docker --location="$BATCHLENS_REGION" --project="$BATCHLENS_PROJECT"
  gcloud artifacts repositories add-iam-policy-binding batchlens --location="$BATCHLENS_REGION" --project="$BATCHLENS_PROJECT" --member="serviceAccount:$BATCHLENS_BUILDER" --role=roles/artifactregistry.writer --quiet >/dev/null
  gcloud storage buckets describe "gs://$BATCHLENS_BUCKET" --project="$BATCHLENS_PROJECT" >/dev/null 2>&1 || gcloud storage buckets create "gs://$BATCHLENS_BUCKET" --location="$BATCHLENS_REGION" --uniform-bucket-level-access --project="$BATCHLENS_PROJECT"
  gcloud storage buckets add-iam-policy-binding "gs://$BATCHLENS_BUCKET" --member="serviceAccount:$BATCHLENS_BUILDER" --role=roles/storage.objectViewer --quiet >/dev/null
  gcloud firestore databases describe --database=batchlens --project="$BATCHLENS_PROJECT" >/dev/null 2>&1 || gcloud firestore databases create --database=batchlens --location="$BATCHLENS_REGION" --type=firestore-native --project="$BATCHLENS_PROJECT"
  gcloud firestore fields ttls update expires_at --database=batchlens --collection-group=batchlens_cases --enable-ttl --project="$BATCHLENS_PROJECT" --quiet
  ;;
 deploy)
  gcloud builds submit . --gcs-source-staging-dir="gs://$BATCHLENS_BUCKET/source" --config=deploy/cloudbuild.yaml --substitutions="_IMAGE=$BATCHLENS_IMAGE" --service-account="projects/$BATCHLENS_PROJECT/serviceAccounts/$BATCHLENS_BUILDER" --project="$BATCHLENS_PROJECT" --quiet
  gcloud run deploy batchlens --image="$BATCHLENS_IMAGE" --region="$BATCHLENS_REGION" --project="$BATCHLENS_PROJECT" --service-account="$BATCHLENS_RUNTIME" --no-allow-unauthenticated --ingress=all --cpu=1 --memory=512Mi --concurrency=20 --min-instances=0 --max-instances=2 --timeout=120 --set-env-vars="STORAGE_BACKEND=firestore,FIRESTORE_DATABASE=batchlens,COOKIE_SECURE=true,GOOGLE_CLOUD_PROJECT=$BATCHLENS_PROJECT,GOOGLE_CLOUD_LOCATION=global,MODEL_ID=$BATCHLENS_MODEL,DAILY_MODEL_CALL_LIMIT=100" --quiet
  ;;
 publish)
  gcloud run services add-iam-policy-binding batchlens --region="$BATCHLENS_REGION" --project="$BATCHLENS_PROJECT" --member=allUsers --role=roles/run.invoker --quiet
  gcloud run services describe batchlens --region="$BATCHLENS_REGION" --project="$BATCHLENS_PROJECT" --format='value(status.url)'
  ;;
 *) echo 'Usage: bash deploy/cloudrun.sh setup|deploy|publish' >&2; exit 2 ;;
esac
