resource "azurerm_resource_group" "rg" {
  name     = var.nombre_grupo_recursos
  location = var.localizacion_grupo_recursos
}