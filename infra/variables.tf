variable "project" {
  description = "Short project slug used to name resources (lowercase alphanumeric/hyphen)."
  type        = string
  default     = "agenticeng"

  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{2,20}$", var.project))
    error_message = "project must be 3-21 chars, lowercase letters/digits/hyphens, starting with a letter."
  }
}

variable "environment" {
  description = "Deployment environment (staging or production)."
  type        = string

  validation {
    condition     = contains(["staging", "production"], var.environment)
    error_message = "environment must be either 'staging' or 'production'."
  }
}

variable "location" {
  description = "Azure region."
  type        = string
  default     = "uaenorth"
}

variable "backend_image" {
  description = "Container image for the backend. A placeholder is used on first apply; the real image is rolled by the deploy workflow via 'az containerapp update'."
  type        = string
  default     = "mcr.microsoft.com/azuredocs/containerapps-helloworld:latest"
}

variable "frontend_image" {
  description = "Container image for the frontend (see backend_image note)."
  type        = string
  default     = "mcr.microsoft.com/azuredocs/containerapps-helloworld:latest"
}

variable "backend_cpu" {
  description = "vCPU allotted to the backend container."
  type        = number
  default     = 0.25
}

variable "backend_memory" {
  description = "Memory allotted to the backend container (must pair with cpu)."
  type        = string
  default     = "0.5Gi"
}

variable "frontend_cpu" {
  description = "vCPU allotted to the frontend container."
  type        = number
  default     = 0.25
}

variable "frontend_memory" {
  description = "Memory allotted to the frontend container (must pair with cpu)."
  type        = string
  default     = "0.5Gi"
}

variable "min_replicas" {
  description = "Minimum replicas per app (0 enables scale-to-zero)."
  type        = number
  default     = 0
}

variable "max_replicas" {
  description = "Maximum replicas per app."
  type        = number
  default     = 2
}

variable "log_retention_days" {
  description = "Log Analytics retention in days."
  type        = number
  default     = 30
}

variable "tags" {
  description = "Additional resource tags."
  type        = map(string)
  default     = {}
}
