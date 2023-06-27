resource "google_cloudiot_registry" "mendoponics_main" {
  name          = "mendoponics-main"
  region        = "us-central1"
  project       = "mendoponics-383115"
  event_notification_configs {
    pubsub_topic_name = "projects/mendoponics-383115/topics/main"
  }
}

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


