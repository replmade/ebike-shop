# ebike-shop Infrastructure

Terraform configuration to deploy the ebike-shop app to a Linode nanode.

## Architecture

- **Linode Nanode (1 GB)** — Ubuntu 24.04
- **Gunicorn** — WSGI server for Django (unix socket)
- **Nginx** — reverse proxy, static files, TLS termination
- **SQLite** — database (dev-friendly, fine for demo traffic)
- **Cloud-init** — fully automated provisioning on first boot

## Quick Start

```bash
cd infra/

# 1. Copy and fill in your values
cp terraform.tfvars.example terraform.tfvars

# 2. Generate a Django secret key
python3 -c 'import secrets; print(secrets.token_urlsafe(50))'
# → paste into terraform.tfvars as django_secret_key

# 3. Init Terraform
terraform init

# 4. Review the plan
terraform plan

# 5. Apply — provisions the nanode, runs cloud-init, deploys the app
terraform apply
```

After `apply` completes, Terraform outputs the IP and SSH command. Wait ~3-5 minutes for cloud-init to finish, then visit `http://<IP>`.

## TLS / HTTPS

If you set `domain` in `terraform.tfvars`, cloud-init will attempt to provision a Let's Encrypt cert via certbot. Make sure DNS is pointed at the Linode IP **before** applying, or run certbot manually after:

```bash
ssh root@<IP>
certbot --nginx -d your-domain.com
```

## Deploying Updates

SSH into the server and run the deploy script:

```bash
ssh root@<IP>
ebike-deploy          # defaults to master
ebike-deploy staging  # or any branch
```

## Destroying

```bash
terraform destroy
```

## Files

| File | Purpose |
|------|---------|
| `main.tf` | Linode instance, firewall, SSH key, outputs |
| `variables.tf` | All input variables with defaults |
| `versions.tf` | Terraform & provider version constraints |
| `cloud-init.yaml.tpl` | Server bootstrap: packages, Gunicorn, Nginx, deploy script |
| `terraform.tfvars.example` | Template for your secrets — **never commit the real .tfvars** |
| `.gitignore` | Excludes state, secrets, and `.terraform/` |

## Cost Estimate

Linode Nanode 1 GB ≈ **$5/month** at time of writing.