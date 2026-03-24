variable "location" {
  description = "Azure region for deployed resources"
  type        = string
  default     = "westeurope"
}

variable "resource_group_name" {
  description = "Name of the Azure resource group"
  type        = string
  default     = "rg-event-driven-automation-platform"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "dev"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "eventdrivenautomationplatform"
}

variable "container_app_name" {
  description = "Container App name"
  type        = string
  default     = "ca-event-driven-automation-platform"
}

variable "container_port" {
  description = "Application container port"
  type        = number
  default     = 8000
}

variable "container_cpu" {
  description = "CPU allocated to the container"
  type        = number
  default     = 0.5
}

variable "container_memory" {
  description = "Memory allocated to the container"
  type        = string
  default     = "1Gi"
}

variable "container_image" {
  description = "Container image to deploy"
  type        = string
  default     = "nginx:latest"
}
