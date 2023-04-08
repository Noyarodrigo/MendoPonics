resource "google_cloudiot_registry" "mendoponics_main" {
  name          = "mendoponics-main"
  region        = "us-central1"
  project       = "mendoponics-383115"
  event_notification_configs {
    pubsub_topic_name = "projects/mendoponics-383115/topics/main"
  }
}

