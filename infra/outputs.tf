output "resource_group_name" {
  description = "Name of the resource group."
  value       = azurerm_resource_group.main.name
}

output "acr_name" {
  description = "Azure Container Registry name (used by 'az acr login')."
  value       = azurerm_container_registry.main.name
}

output "acr_login_server" {
  description = "ACR login server, e.g. myregistry.azurecr.io."
  value       = azurerm_container_registry.main.login_server
}

output "backend_app_name" {
  description = "Name of the backend container app (for 'az containerapp update')."
  value       = azurerm_container_app.backend.name
}

output "frontend_app_name" {
  description = "Name of the frontend container app."
  value       = azurerm_container_app.frontend.name
}

output "backend_url" {
  description = "Public URL of the backend."
  value       = "https://${azurerm_container_app.backend.ingress[0].fqdn}"
}

output "frontend_url" {
  description = "Public URL of the frontend."
  value       = "https://${azurerm_container_app.frontend.ingress[0].fqdn}"
}
