variable "app_image_tag" {
  description = "Tag de l'image Docker de l'application"
  type        = string
  default     = "latest"
}

variable "app_port" {
  description = "Port exposé sur l'hôte pour l'application"
  type        = number
  default     = 5000
}
