resource "azurerm_resource_group" "rg" {
  name     = var.nombre_grupo_recursos
  location = var.localizacion_grupo_recursos
}

resource "azurerm_log_analytics_workspace" "log_analytics" {
  name                = var.nombre_log_analytics
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

resource "azurerm_container_app_environment" "apps_environment" {
  name                       = var.nombre_entorno_apps
  location                   = var.localizacion_grupo_recursos
  resource_group_name        = azurerm_resource_group.rg.name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.log_analytics.id

}

resource "azurerm_container_app" "app" {
  name                         = var.nombre_app
  container_app_environment_id = azurerm_container_app_environment.apps_environment.id
  resource_group_name          = azurerm_resource_group.rg.name
  revision_mode                = "Single"

  template {
    container {
      name   = var.nombre_contenedor
      image  = var.nombre_imagen_contenedor
      cpu    = 0.5
      memory = "1.0Gi"

      env {
        name        = "ENTORNO"
        secret_name = "entorno"
      }

    }
  }

  secret {
    name  = "entorno"
    value = var.entorno
  }

  ingress {
    external_enabled = true
    target_port      = 5000

    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }
}