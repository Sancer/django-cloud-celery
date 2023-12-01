## Provisioning, Migrations, and Deployment

1. Create project with billing enabled, and configure gcloud for that project

   ```
   PROJECT_ID=<your_project_id>
   gcloud config set project $PROJECT_ID
   ```

1. Configure default credentials (allows Terraform to apply changes):

   ```
   gcloud auth application-default login
   ```

1. Enable base services:

   ```
   gcloud services enable \
     cloudbuild.googleapis.com \
     run.googleapis.com \
     cloudresourcemanager.googleapis.com
   ```

1. Build base image

   ```
   make build
   ```


1. Run database migrations

   ```
   make deploy