

build:
	gcloud builds submit --config cloudbuild-ci.yaml


deploy:
	sh ./deploy.sh
