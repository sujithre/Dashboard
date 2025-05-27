# Configure the Azure provider
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }

  backend "azurerm" {
    resource_group_name  = "rg-terraform-state"
    storage_account_name = "tfstatenovartis"
    container_name      = "tfstate"
    key                 = "novartis.terraform.tfstate"
  }
}

provider "azurerm" {
  features {}
}

# Variables
variable "project" {
  type        = string
  description = "Project name"
  default     = "novartis"
}

variable "environment" {
  type        = string
  description = "Environment (dev, prod, etc.)"
  default     = "dev"
}

variable "location" {
  type        = string
  description = "Azure region"
  default     = "westeurope"
}

# Resource Group
resource "azurerm_resource_group" "rg" {
  name     = "rg-${var.project}-${var.environment}"
  location = var.location

  tags = {
    Environment = var.environment
    Project     = var.project
  }
}

# Azure Container Registry
resource "azurerm_container_registry" "acr" {
  name                = "acr${var.project}${var.environment}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                = "Standard"
  admin_enabled      = true

  tags = {
    Environment = var.environment
    Project     = var.project
  }
}

# Log Analytics Workspace
resource "azurerm_log_analytics_workspace" "law" {
  name                = "law-${var.project}-${var.environment}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                = "PerGB2018"
  retention_in_days   = 30

  tags = {
    Environment = var.environment
    Project     = var.project
  }
}

# Container App Environment
resource "azurerm_container_app_environment" "env" {
  name                       = "cae-${var.project}-${var.environment}"
  location                   = azurerm_resource_group.rg.location
  resource_group_name        = azurerm_resource_group.rg.name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.law.id

  tags = {
    Environment = var.environment
    Project     = var.project
  }
}

# Container App
resource "azurerm_container_app" "app" {
  name                         = "ca-${var.project}-${var.environment}"
  container_app_environment_id = azurerm_container_app_environment.env.id
  resource_group_name         = azurerm_resource_group.rg.name
  revision_mode               = "Single"

  template {
    container {
      name   = "costdashboard"
      image  = "${azurerm_container_registry.acr.login_server}/${var.project}:latest"
      cpu    = "0.5"
      memory = "1Gi"

      env {
        name  = "FLASK_APP"
        value = "app.py"
      }

      env {
        name  = "FLASK_ENV"
        value = "production"
      }
    }
  }

  ingress {
    external_enabled = true
    target_port     = 8000
    transport       = "auto"

    traffic_weight {
      latest_revision = true
      percentage      = 100
    }
  }

  registry {
    server               = azurerm_container_registry.acr.login_server
    username            = azurerm_container_registry.acr.admin_username
    password_secret_name = "registry-password"
  }

  secret {
    name  = "registry-password"
    value = azurerm_container_registry.acr.admin_password
  }

  tags = {
    Environment = var.environment
    Project     = var.project
  }
}

# Outputs
output "acr_login_server" {
  value = azurerm_container_registry.acr.login_server
}

output "container_app_url" {
  value = azurerm_container_app.app.latest_revision_fqdn
}
