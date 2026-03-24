output "resource_group_name" {
  description = "Resource group name"
  value       = azurerm_resource_group.this.name
}

output "resource_group_location" {
  description = "Resource group location"
  value       = azurerm_resource_group.this.location
}

output "acr_login_server" {
  description = "Azure Container Registry login server"
  value       = azurerm_container_registry.this.login_server
}

output "container_app_name" {
  description = "Azure Container App name"
  value       = azurerm_container_app.this.name
}

output "container_app_url" {
  description = "Azure Container App public URL"
  value       = azurerm_container_app.this.latest_revision_fqdn
}
