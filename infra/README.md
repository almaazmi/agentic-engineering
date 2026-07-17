# Infrastructure — Terraform + Azure Container Apps

Provisions the platform that runs the backend and frontend:

```
Resource Group
├── Log Analytics Workspace        (container logs/metrics)
├── Azure Container Registry (ACR)  (Basic, admin disabled)
├── User-Assigned Managed Identity  (AcrPull — apps pull images)
└── Container Apps Environment
    ├── Container App: backend      (ingress :8000, /health probes)
    └── Container App: frontend     (ingress :3000, BACKEND_URL -> backend)
```

## Design notes

- **State**: remote in Azure Storage (`backend "azurerm"`), configured at
  `init` time via `-backend-config`. Each environment uses a distinct state
  **key** (`staging.tfstate`, `production.tfstate`) against the same storage
  account, so one codebase serves all environments.
- **Auth**: GitHub Actions authenticate to Azure with **OIDC federated
  credentials** — no long-lived secrets. See the root `README.md`.
- **Infra vs. release**: Terraform owns infrastructure; the container **image**
  is rolled by the deploy workflow (`az containerapp update`). The image field
  is under `ignore_changes` so the two never fight. First apply uses a public
  placeholder image.

## One-time bootstrap (creates the state backend)

```bash
az group create -n tfstate-rg -l uaenorth
az storage account create -n <UNIQUE_SA_NAME> -g tfstate-rg -l uaenorth --sku Standard_LRS
az storage container create -n tfstate --account-name <UNIQUE_SA_NAME>
```

## Plan/apply locally (staging)

```bash
cd infra
terraform init \
  -backend-config="resource_group_name=tfstate-rg" \
  -backend-config="storage_account_name=<UNIQUE_SA_NAME>" \
  -backend-config="container_name=tfstate" \
  -backend-config="key=staging.tfstate"

terraform plan  -var-file=environments/staging.tfvars
terraform apply -var-file=environments/staging.tfvars
```

Required environment variables (set by CI from GitHub secrets):
`ARM_CLIENT_ID`, `ARM_TENANT_ID`, `ARM_SUBSCRIPTION_ID`, and `ARM_USE_OIDC=true`.

## Valid CPU/memory pairs

Azure Container Apps only accept specific combinations, e.g. `0.25/0.5Gi`,
`0.5/1Gi`, `0.75/1.5Gi`, `1.0/2Gi`.
