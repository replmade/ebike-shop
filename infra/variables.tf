# ─── Linode provider ───

variable "linode_token" {
  description = "Linode API token (set via LINODE_TOKEN env var or terraform.tfvars)"
  type        = string
  sensitive   = true
}

variable "linode_region" {
  description = "Linode data center region"
  type        = string
  default     = "us-east"
}

# ─── Instance ───

variable "instance_type" {
  description = "Linode plan slug (e.g. g6-nanode-1)"
  type        = string
  default     = "g6-nanode-1"
}

variable "instance_label" {
  description = "Label for the Linode instance"
  type        = string
  default     = "ebike-shop"
}

variable "ssh_public_key" {
  description = "SSH public key to authorize on the instance"
  type        = string
}

variable "ssh_private_key_path" {
  description = "Path to the SSH private key for provisioning (local only)"
  type        = string
  default     = "~/.ssh/id_ed25519"
}

# ─── App ───

variable "domain" {
  description = "Domain name for the app (e.g. ebike-shop.example.com). Leave empty to use the Linode IP directly."
  type        = string
  default     = ""
}

variable "django_secret_key" {
  description = "Secret key for Django (generate with: python -c 'import secrets; print(secrets.token_urlsafe(50))')"
  type        = string
  sensitive   = true
}

variable "django_superuser_email" {
  description = "Email for the Django admin superuser"
  type        = string
  default     = "admin@voltcycle.com"
}

variable "django_superuser_password" {
  description = "Password for the Django admin superuser"
  type        = string
  sensitive   = true
}

variable "repo_url" {
  description = "Git repository URL to clone on the server"
  type        = string
  default     = "https://github.com/replmade/ebike-shop.git"
}

variable "repo_branch" {
  description = "Git branch to deploy"
  type        = string
  default     = "master"
}