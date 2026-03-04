
# ----- Resource group -----
resource "azurerm_resource_group" "rg" {
  name     = "rg-${var.project_name}"
  location = var.location
}


# ----- Storage account (Blob) -----
resource "azurerm_storage_account" "storage" {
  name                     = "st${replace(var.project_name, "-", "")}"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  allow_nested_items_to_be_public = false
}


# ----- Private container for images -----
resource "azurerm_storage_container" "images" {
  name                  = "generated-images"
  storage_account_name  = azurerm_storage_account.storage.name
  container_access_type = "private"
}