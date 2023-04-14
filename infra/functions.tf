
resource "google_cloudfunctions_function" "device_handler" {
  name        = "device_handler"
  description = "Function triggered by Pub/Sub topic 'main' for device management"
  runtime     = "python37"
  entry_point = "device_handler"
  available_memory_mb = 128
  source_archive_bucket = "functions_mendoponics"
  source_archive_object = "pubsub-devicehandler.zip"

 environment_variables = {
    dataset = "main"
    table   = "measurements"
  }

  event_trigger {
    event_type = "google.pubsub.topic.publish"
    resource = "projects/mendoponics-383115/topics/main"
    failure_policy {
      retry = false
    }
  }
}

resource "google_cloudfunctions_function" "alert_handler" {
  name        = "alert_handler"
  description = "Function triggered by Pub/Sub topic 'alerts' for sending email alerts"
  runtime     = "python37"
  entry_point = "alert_handler"
  available_memory_mb = 128
  source_archive_bucket = "functions_mendoponics"
  source_archive_object = "pubsub-alerthandler.zip"

 environment_variables = {
    dataset = "main"
    table   = "alerts"
  }

  event_trigger {
    event_type = "google.pubsub.topic.publish"
    resource = "projects/mendoponics-383115/topics/alerts"
    failure_policy {
      retry = false
    }
  }
}

resource "google_cloudfunctions_function" "pump_handler" {
  name        = "pump_handler"
  description = "Function triggered by Pub/Sub topic 'pump' for actuators management"
  runtime     = "python37"
  entry_point = "actuator_handler"
  available_memory_mb = 128
  source_archive_bucket = "functions_mendoponics"
  source_archive_object = "pubsub-actuatorhandler.zip"

 environment_variables = {
    dataset = "main"
  }

  event_trigger {
    event_type = "google.pubsub.topic.publish"
    resource = "projects/mendoponics-383115/topics/pump"
    failure_policy {
      retry = false
    }
  }

}
resource "google_cloudfunctions_function" "light_handler" {
  name        = "light_handler"
  description = "Function triggered by Pub/Sub topic 'light' for actuators management"
  runtime     = "python37"
  entry_point = "actuator_handler"
  available_memory_mb = 128
  source_archive_bucket = "functions_mendoponics"
  source_archive_object = "pubsub-actuatorhandler.zip"

 environment_variables = {
    dataset = "main"
  }

  event_trigger {
    event_type = "google.pubsub.topic.publish"
    resource = "projects/mendoponics-383115/topics/light"
    failure_policy {
      retry = false
    }
  }

}
