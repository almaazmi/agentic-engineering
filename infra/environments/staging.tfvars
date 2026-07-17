# Staging environment. Optimised for cost: scale-to-zero, small containers.
environment  = "staging"
location     = "uaenorth"
min_replicas = 0
max_replicas = 1

backend_cpu     = 0.25
backend_memory  = "0.5Gi"
frontend_cpu    = 0.25
frontend_memory = "0.5Gi"

log_retention_days = 30

tags = {
  cost_center = "engineering"
  tier        = "staging"
}
