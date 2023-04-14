resource "google_pubsub_topic" "main_topic" {
  name = "main"
}

resource "google_pubsub_topic" "alerts_topic" {
  name = "alerts"
}

resource "google_pubsub_topic" "pump_topic" {
  name = "pump"
}

resource "google_pubsub_topic" "light_topic" {
  name = "light"
}
