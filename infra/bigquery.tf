resource "google_bigquery_dataset" "main" {
  dataset_id                   = "main"
  location                     = "US"
}

resource "google_bigquery_table" "alerts" {
  dataset_id = google_bigquery_dataset.main.dataset_id
  table_id   = "alerts"

  schema = <<SCHEMA
[
  {"name": "timestamp", "type": "TIMESTAMP", "mode": "REQUIRED"},
  {"name": "deviceid", "type": "STRING", "mode": "REQUIRED"},
  {"name": "priority", "type": "INTEGER", "mode": "REQUIRED"},
  {"name": "message", "type": "STRING", "mode": "REQUIRED"},
  {"name": "email", "type": "STRING", "mode": "REQUIRED"}
]
SCHEMA
}

resource "google_bigquery_table" "configurations" {
  dataset_id = google_bigquery_dataset.main.dataset_id
  table_id   = "configurations"

  schema = <<SCHEMA
[
  {"name": "timestamp", "type": "TIMESTAMP", "mode": "REQUIRED"},
  {"name": "deviceid", "type": "STRING", "mode": "REQUIRED"},
  {"name": "sunrise", "type": "INTEGER", "mode": "REQUIRED"},
  {"name": "sunset", "type": "INTEGER", "mode": "REQUIRED"},
  {"name": "pump_interval", "type": "INTEGER", "mode": "REQUIRED"},
  {"name": "pump_timeon", "type": "INTEGER", "mode": "REQUIRED"},
  {"name": "description", "type": "STRING", "mode": "REQUIRED"},
  {"name": "location", "type": "STRING", "mode": "REQUIRED"},
  {"name": "registry", "type": "STRING", "mode": "REQUIRED"}
]
SCHEMA
}

resource "google_bigquery_table" "devices" {
  dataset_id = google_bigquery_dataset.main.dataset_id
  table_id   = "devices"

  schema = <<SCHEMA
[
  {"name": "deviceid", "type": "STRING", "mode": "REQUIRED"},
  {"name": "owner", "type": "STRING", "mode": "REQUIRED"}
]
SCHEMA
}

resource "google_bigquery_table" "measurements" {
  dataset_id = google_bigquery_dataset.main.dataset_id
  table_id   = "measurements"

  schema = <<SCHEMA
[
  {"name": "tmpambiente", "type": "FLOAT", "mode": "NULLABLE"},
  {"name": "humedad", "type": "FLOAT", "mode": "NULLABLE"},
  {"name": "luz", "type": "FLOAT", "mode": "NULLABLE"},
  {"name": "tmpagua", "type": "FLOAT", "mode": "NULLABLE"},
  {"name": "timestamp", "type": "TIMESTAMP", "mode": "REQUIRED"},
  {"name": "email", "type": "STRING", "mode": "REQUIRED"},
  {"name": "deviceid", "type": "STRING", "mode": "REQUIRED"}
]
SCHEMA
}

resource "google_bigquery_table" "waterquality" {
  dataset_id = google_bigquery_dataset.main.dataset_id
  table_id   = "waterquality"

  schema = <<SCHEMA
[
  {"name": "timestamp", "type": "TIMESTAMP", "mode": "REQUIRED"},
  {"name": "deviceid", "type": "STRING", "mode": "REQUIRED"},
  {"name": "email", "type": "STRING", "mode": "REQUIRED"},
  {"name": "ph", "type": "FLOAT", "mode": "REQUIRED"},
  {"name": "ppm", "type": "FLOAT", "mode": "REQUIRED"}
]
SCHEMA
}
resource "google_bigquery_table" "pumpstatus" {
  dataset_id = google_bigquery_dataset.main.dataset_id
  table_id   = "pumpstatus"

  schema = <<EOF
[
  {
    "name": "timestamp",
    "type": "TIMESTAMP"
  },
  {
    "name": "email",
    "type": "STRING"
  },
  {
    "name": "pump",
    "type": "INTEGER"
  },

  {"name": "deviceid", "type": "STRING", "mode": "REQUIRED"}
]
EOF
}

resource "google_bigquery_table" "lightstatus" {
  dataset_id = google_bigquery_dataset.main.dataset_id
  table_id   = "lightstatus"

  schema = <<EOF
[
  {
    "name": "timestamp",
    "type": "TIMESTAMP"
  },
  {
    "name": "email",
    "type": "STRING"
  },
  {
    "name": "light",
    "type": "INTEGER"
  },
  {"name": "deviceid", "type": "STRING", "mode": "REQUIRED"}
]
EOF
}
