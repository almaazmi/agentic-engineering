# Production environment. Always-on with headroom to scale out.
environment  = "production"
location     = "uaenorth"
min_replicas = 1
max_replicas = 3

backend_cpu     = 0.5
backend_memory  = "1Gi"
frontend_cpu    = 0.5
frontend_memory = "1Gi"

log_retention_days = 90

tags = {
  cost_center = "engineering"
  tier        = "production"
}
