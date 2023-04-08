resource "google_iot_device" "htd1" {
  device_id        = "htd1"
  registry_id      = google_iot_registry.registry.id
  public_key {
    format     = "ES256_PEM"
    key        = file("../access-keys/ec_public.pem")
  }
}

resource "google_iot_device" "htd2" {
  device_id        = "htd2"
  registry_id      = google_iot_registry.registry.id
  public_key {
    format     = "ES256_PEM"
    key        = file("../access-keys/ec_public.pem")
  }
}

