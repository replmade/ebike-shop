# ─── Provider ───

provider "linode" {
  token = var.linode_token
}

# ─── SSH key ───

resource "linode_sshkey" "deploy_key" {
  label   = "${var.instance_label}-deploy"
  ssh_key = var.ssh_public_key
}

# ─── Firewall ───

resource "linode_firewall" "app" {
  label           = "${var.instance_label}-fw"
  inbound_policy  = "DROP"
  outbound_policy = "ACCEPT"

  inbound {
    label    = "ssh"
    action   = "ACCEPT"
    protocol = "TCP"
    ports    = "22"
    ipv4     = ["0.0.0.0/0"]
    ipv6     = ["::/0"]
  }

  inbound {
    label    = "http"
    action   = "ACCEPT"
    protocol = "TCP"
    ports    = "80"
    ipv4     = ["0.0.0.0/0"]
    ipv6     = ["::/0"]
  }

  inbound {
    label    = "https"
    action   = "ACCEPT"
    protocol = "TCP"
    ports    = "443"
    ipv4     = ["0.0.0.0/0"]
    ipv6     = ["::/0"]
  }

}

# ─── Instance ───

resource "linode_instance" "app" {
  label           = var.instance_label
  image           = "linode/ubuntu24.04"
  region          = var.linode_region
  type            = var.instance_type
  authorized_keys = [linode_sshkey.deploy_key.ssh_key]
  firewall_id     = linode_firewall.app.id
  tags            = ["ebike-shop", "production"]

  # Cloud-init: bootstrap the server on first boot
  user_data = templatefile("${path.module}/cloud-init.yaml.tpl", {
    django_secret_key         = var.django_secret_key
    django_superuser_email    = var.django_superuser_email
    django_superuser_password = var.django_superuser_password
    domain                    = var.domain
    repo_url                  = var.repo_url
    repo_branch               = var.repo_branch
  })
}

# ─── Outputs ───

output "instance_ip" {
  value = linode_instance.app.ip_address
}

output "instance_id" {
  value = linode_instance.app.id
}

output "ssh_command" {
  value = "ssh root@${linode_instance.app.ip_address}"
}