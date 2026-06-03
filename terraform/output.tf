output "container_app_url" {
  value       = "https://${azurerm_container_app.app.ingress[0].fqdn}"
  description = "URL del Container App"
}

output "nombre_storage_account" {
  value       = azurerm_storage_account.storage_account.name
  description = "Nombre del Storage Account"
}

output "nombre_service_plan" {
  value       = azurerm_service_plan.service_plan.name
  description = "Nombre del service plan"
}

output "nombre_az_function" {
  value       = azurerm_linux_function_app.azure_function.name
  description = "Nombre del Azure Function"
}

output "az_function_url" {
  value       = "https://${azurerm_linux_function_app.azure_function.name}.azurewebsites.net"
  description = "URL pública del Azure Function"
}