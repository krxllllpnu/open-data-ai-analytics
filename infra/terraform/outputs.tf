output "public_ip" {
  description = "Public IP address of the created VM."
  value       = azurerm_public_ip.public_ip.ip_address
}

output "web_url" {
  description = "URL for checking the web interface."
  value       = "http://${azurerm_public_ip.public_ip.ip_address}:${var.app_port}"
}

output "ssh_command" {
  description = "SSH command for optional manual debugging."
  value       = "ssh ${var.admin_username}@${azurerm_public_ip.public_ip.ip_address}"
}