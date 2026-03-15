
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

  # We have to allow nested items to be public, as the container
  # for the generated images will need to be accessed by the 
  # instagram publisher to retrieve the images and publish them.
  allow_nested_items_to_be_public = true
}


# ----- Public container for images -----
# The container has to provide public read access to blobs for the
# instagram publisher to be able to retrieve them and publish them.
resource "azurerm_storage_container" "images" {
  name                  = "generated-images"
  storage_account_name  = azurerm_storage_account.storage.name
  container_access_type = "blob"
}