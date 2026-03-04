1. Setup Azure
    1. Create an azure subscription
    2. Install Azure CLI in your PC. In powershell, call `winget install --exact --id Microsoft.AzureCLI`
    3. Login to Azure with the Azure cli `az login`  
    4. Verify you are properly logged in and that your subscription is active with `az account show`
    5. Set your subscription with `az account set --subscription "<your subscription ID>"`. You can find your ID under the Azure resource Subscriptions
-- If you are not logged in with the Azure CLI, Terraform will not work!



2. Setup Terraform
2.1. Install Terraform from https://developer.hashicorp.com/terraform
2.2. Add Terraform to your system path
2.3. Check terraform is properly installed by typing in a command line `Terraform --version`

3. Run Terraform
Run on cmd
```
terraform init
terraform plan
terraform apply
```

These actions should be carried out by the CI/CD in the future

