resource "google_compute_instance" "free_tier_instance" {
  name         = "mendoponics-main"
  machine_type = "e2-micro"
  zone         = "us-central1-a"
  
  boot_disk {
    initialize_params {
      size  = 30
      image = "ubuntu-os-cloud/ubuntu-2004-lts"
      type  = "pd-standard"
    }
  }

  network_interface {
    access_config {
    }
  }

  metadata = {
    ssh-keys = file("~/.ssh/id_rsa.pub")
  }

  tags = ["http-server", "https-server"]
}

resource "google_compute_firewall" "free_tier_firewall" {
  name    = "free-tier-firewall"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["80", "443"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["http-server", "https-server"]
}

