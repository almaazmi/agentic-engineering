terraform {
  required_version = ">= 1.9.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 5.2"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
  }

  # Remote state in Azure Storage. Configured at init time via -backend-config
  # (see .github/workflows/*deploy* and infra/README.md) so the same code serves
  # every environment with a different state key.
  backend "azurerm" {}
}
