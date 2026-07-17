provider "azurerm" {
  # subscription_id is supplied via the ARM_SUBSCRIPTION_ID environment
  # variable (set from the AZURE_SUBSCRIPTION_ID GitHub secret in CI).
  features {
    resource_group {
      prevent_deletion_if_contains_resources = false
    }
  }
}
