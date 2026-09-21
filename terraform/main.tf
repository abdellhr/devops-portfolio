terraform {
  required_version = ">= 1.7.0"
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {}

resource "docker_network" "devops_net" {
  name = "devops-portfolio-net"
}

resource "docker_image" "app" {
  name = "devops-portfolio-app:${var.app_image_tag}"
  build {
    context = "${path.module}/../app"
  }
}

resource "docker_container" "app" {
  name  = "devops-portfolio-app"
  image = docker_image.app.image_id

  networks_advanced {
    name = docker_network.devops_net.name
  }

  ports {
    internal = 5000
    external = var.app_port
  }

  healthcheck {
    test     = ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"]
    interval = "30s"
    timeout  = "3s"
    retries  = 3
  }
}
