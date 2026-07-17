locals {
  # ACR names must be globally unique and alphanumeric only.
  acr_name = "${replace(var.project, "-", "")}${var.environment}${random_string.suffix.result}"

  name = "${var.project}-${var.environment}"

  common_tags = merge(
    {
      project     = var.project
      environment = var.environment
      managed_by  = "terraform"
      repo        = "agentic-engineering"
    },
    var.tags,
  )
}
