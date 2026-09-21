output "container_name" {
  description = "Nom du conteneur applicatif déployé"
  value       = docker_container.app.name
}

output "app_url" {
  description = "URL locale pour accéder à l'application"
  value       = "http://localhost:${var.app_port}"
}
