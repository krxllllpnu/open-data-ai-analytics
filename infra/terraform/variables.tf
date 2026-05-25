variable "project_name" {
  description = "Prefix for Azure resources."
  type        = string
  default     = "open-data-ai-analytics"
}

variable "location" {
  description = "Azure region."
  type        = string
  default     = "swedencentral"
}

variable "vm_size" {
  description = "VM size."
  type        = string
  default     = "Standard_B2s_v2"
}

variable "admin_username" {
  description = "Linux VM admin user."
  type        = string
  default     = "azureuser"
}

variable "ssh_public_key_path" {
  description = "Path to SSH public key."
  type        = string
  default     = "~/.ssh/id_rsa.pub"
}

variable "repo_url" {
  description = "GitHub repository URL with Docker project."
  type        = string
  default     = "https://github.com/krxllllpnu/open-data-ai-analytics.git"
}

variable "compose_file" {
  description = "Path to compose file inside repository."
  type        = string
  default     = "compose.yaml"
}

variable "app_port" {
  description = "Port exposed by the web interface."
  type        = number
  default     = 8080
}

variable "gitops_node_port" {
  description = "NodePort used by the GitOps-managed Kubernetes web service."
  type        = number
  default     = 30080
}
