resource "google_pubsub_topic" "main_topic" {
  name = "main"
}

resource "google_pubsub_topic" "alerts_topic" {
  name = "alerts"
}

