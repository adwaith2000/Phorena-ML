project = "temperature_sensor"

app "temperature_sensor" {
  labels = {
      "service" = "temperature_sensor",
      "env" = "dev"
  }

  build {
    use "docker" {
    }
 }

  deploy { 
    use "kubernetes" {
    }
  }
}