output "public_ip" {
  description = "Public IP address of the created VM."
  value       = azurerm_public_ip.public_ip.ip_address
}

output "web_url" {
  description = "URL for checking the web interface. (Assuming the web service is started using docker compose profile.)"
  value       = "http://${azurerm_public_ip.public_ip.ip_address}:${var.app_port}"
}

output "gitops_app_url" {
  description = "URL for checking the Argo CD managed Kubernetes NodePort web service."
  value       = "http://${azurerm_public_ip.public_ip.ip_address}:${var.gitops_node_port}"
}

output "ssh_command" {
  description = "SSH command for optional manual debugging."
  value       = "ssh ${var.admin_username}@${azurerm_public_ip.public_ip.ip_address}"
}
