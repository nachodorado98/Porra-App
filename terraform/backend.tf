terraform {
  backend "azurerm" {
    resource_group_name  = "rg-backend-nacho-golden"
    storage_account_name = "tfstatenachogolden"
    container_name       = "tfstateporra"
    key                  = "terraformnachoporra.tfstate"
  }
}