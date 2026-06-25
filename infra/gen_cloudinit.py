#!/usr/bin/env python3
"""Generate cloud-init.yaml.tpl for Terraform templatefile().

Uses chr() encoding to avoid ${} patterns that the Hermes
write_file tool mangles. Variable names are stored separately
and interpolated at runtime.
"""
import pathlib

DS = chr(36)   # $
OB = chr(123)  # {
CB = chr(125)  # }
Q  = chr(34)   # "
BS = chr(92)   # \

# Build ${var} at runtime from parts to avoid literal ${} in source
def tf(var):
    return DS + OB + var + CB

lines = []

lines.append("#cloud-config")
lines.append("")
lines.append("package_update: true")
lines.append("package_upgrade: true")
lines.append("")
lines.append("packages:")
for p in ["python3", "python3-venv", "python3-pip", "nginx", "git", "certbot", "python3-certbot-nginx"]:
    lines.append("  - " + p)
lines.append("")

lines.append("write_files:")

# .env file
lines.append("  # --- Django production settings override ---")
lines.append("  - path: /opt/ebike-shop/.env")
lines.append("    owner: root:www-data")
lines.append("    permissions: " + Q + "0640" + Q)
lines.append("    content: |")
lines.append("      DJANGO_SECRET_KEY=" + tf("django_secret_key"))
lines.append("      DJANGO_ALLOWED_HOSTS=%{ if domain != " + Q + Q + " }" + tf("domain") + " www." + tf("domain") + "%{ else }*%{ endif }")
lines.append("      DJANGO_DEBUG=False")
lines.append("      DJANGO_SETTINGS_MODULE=shop.settings")
lines.append("")

# Gunicorn systemd unit
lines.append("  # --- Gunicorn systemd unit ---")
lines.append("  - path: /etc/systemd/system/ebike-shop.service")
lines.append("    content: |")
lines.append("      [Unit]")
lines.append("      Description=ebike-shop Gunicorn daemon")
lines.append("      After=network.target")
lines.append("")
lines.append("      [Service]")
lines.append("      User=www-data")
lines.append("      Group=www-data")
lines.append("      WorkingDirectory=/opt/ebike-shop/backend")
lines.append("      EnvironmentFile=/opt/ebike-shop/.env")
lines.append("      ExecStart=/opt/ebike-shop/backend/venv/bin/gunicorn " + BS)
lines.append("          --workers 2 " + BS)
lines.append("          --bind unix:/run/ebike-shop.sock " + BS)
lines.append("          --timeout 120 " + BS)
lines.append("          shop.wsgi:application")
lines.append("      Restart=always")
lines.append("      RestartSec=5")
lines.append("")
lines.append("      [Install]")
lines.append("      WantedBy=multi-user.target")
lines.append("")

# Nginx site config
# NOTE: cloud-init write_files does NOT de-dollar ($$ -> $).
# Use single $ for nginx variables - they're in a | block scalar (literal text).
lines.append("  # --- Nginx site config ---")
lines.append("  - path: /etc/nginx/sites-available/ebike-shop")
lines.append("    content: |")
lines.append("      server {")
lines.append("          listen 80;")
lines.append("          server_name %{ if domain != " + Q + Q + " }" + tf("domain") + " www." + tf("domain") + "%{ else }_%{ endif };")
lines.append("")
lines.append("          location / {")
lines.append("              root /opt/ebike-shop/frontend/dist;")
lines.append("              try_files " + DS + "uri " + DS + "uri/ /index.html;")
lines.append("          }")
lines.append("")
lines.append("          location /static/ {")
lines.append("              alias /opt/ebike-shop/backend/staticfiles/;")
lines.append("          }")
lines.append("")
lines.append("          location /api/ {")
lines.append("              proxy_pass http://unix:/run/ebike-shop.sock;")
lines.append("              proxy_set_header Host " + DS + "host;")
lines.append("              proxy_set_header X-Real-IP " + DS + "remote_addr;")
lines.append("              proxy_set_header X-Forwarded-For " + DS + "proxy_add_x_forwarded_for;")
lines.append("              proxy_set_header X-Forwarded-Proto " + DS + "scheme;")
lines.append("          }")
lines.append("")
lines.append("          location /admin/ {")
lines.append("              proxy_pass http://unix:/run/ebike-shop.sock;")
lines.append("              proxy_set_header Host " + DS + "host;")
lines.append("              proxy_set_header X-Real-IP " + DS + "remote_addr;")
lines.append("              proxy_set_header X-Forwarded-For " + DS + "proxy_add_x_forwarded_for;")
lines.append("              proxy_set_header X-Forwarded-Proto " + DS + "scheme;")
lines.append("          }")
lines.append("      }")
lines.append("")

# Deploy script
# NOTE: Same as nginx - single $ for bash vars in write_files content.
lines.append("  # --- Deploy script (also used for future updates) ---")
lines.append("  - path: /usr/local/bin/ebike-deploy")
lines.append("    permissions: " + Q + "0755" + Q)
lines.append("    content: |")
lines.append("      #!/usr/bin/env bash")
lines.append("      set -euo pipefail")
lines.append("")
lines.append("      APP_DIR=/opt/ebike-shop")
lines.append("      BRANCH=" + Q + DS + "{1:-master}" + Q)
lines.append("")
lines.append("      echo " + Q + "=== Pulling latest code (branch: " + DS + "BRANCH) ===" + Q)
lines.append("      cd " + Q + DS + "APP_DIR" + Q)
lines.append("      git fetch origin")
lines.append("      git checkout " + Q + DS + "BRANCH" + Q)
lines.append("      git reset --hard " + Q + "origin/" + DS + "BRANCH" + Q)
lines.append("")
lines.append("      echo " + Q + "=== Setting up backend ===" + Q)
lines.append("      cd " + Q + DS + "APP_DIR/backend" + Q)
lines.append("      if [ ! -d venv ]; then")
lines.append("        python3 -m venv venv")
lines.append("      fi")
lines.append("      source venv/bin/activate")
lines.append("      pip install -r requirements.txt")
lines.append("      python manage.py makemigrations api --noinput")
lines.append("      python manage.py migrate --noinput")
lines.append("      python manage.py collectstatic --noinput")
lines.append("      python manage.py seed_data || true")
lines.append("")
lines.append("      echo " + Q + "=== Setting up frontend ===" + Q)
lines.append("      cd " + Q + DS + "APP_DIR/frontend" + Q)
lines.append("      npm install")
lines.append("      npm run build")
lines.append("")
lines.append("      echo " + Q + "=== Restarting services ===" + Q)
lines.append("      systemctl restart ebike-shop")
lines.append("      systemctl reload nginx")
lines.append("")
lines.append("      echo " + Q + "=== Deploy complete ===" + Q)
lines.append("")

# runcmd
# NOTE: In runcmd, cloud-init DOES de-dollar ($$ -> $) for shell commands.
# But we don't need $$ here since runcmd strings are run by shell directly.
lines.append("runcmd:")
lines.append("  # Clone the repo")
lines.append("  - git clone --branch " + Q + tf("repo_branch") + Q + " " + Q + tf("repo_url") + Q + " /opt/ebike-shop")
lines.append("")
lines.append("  # Initial deploy")
lines.append("  - /usr/local/bin/ebike-deploy " + Q + tf("repo_branch") + Q)
lines.append("")
lines.append("  # Create Django superuser via non-interactive manage.py")
lines.append("  - |")
lines.append("    cd /opt/ebike-shop/backend")
lines.append("    source venv/bin/activate")
lines.append("    DJANGO_SUPERUSER_PASSWORD=" + Q + tf("django_superuser_password") + Q + " " + BS)
lines.append("    DJANGO_SUPERUSER_EMAIL=" + Q + tf("django_superuser_email") + Q + " " + BS)
lines.append("    DJANGO_SUPERUSER_USERNAME=" + Q + tf("django_superuser_email") + Q + " " + BS)
lines.append("    python manage.py createsuperuser --noinput || true")
lines.append("")
lines.append("  # Enable Gunicorn service")
lines.append("  - systemctl enable ebike-shop")
lines.append("  - systemctl start ebike-shop")
lines.append("")
lines.append("  # Enable Nginx site")
lines.append("  - ln -sf /etc/nginx/sites-available/ebike-shop /etc/nginx/sites-enabled/ebike-shop")
lines.append("  - rm -f /etc/nginx/sites-enabled/default")
lines.append("  - systemctl reload nginx")
lines.append("")
# Use |- block scalar for certbot to avoid YAML dict issue
lines.append("  # Provision TLS if a domain is configured")
lines.append("%{ if domain != " + Q + Q + " }")
lines.append("  - |")
lines.append("    certbot --nginx -n --agree-tos -m " + tf("django_superuser_email") + " -d " + tf("domain") + " || echo 'TLS setup failed'")
lines.append("%{ endif }")

content = chr(10).join(lines) + chr(10)

target = pathlib.Path(__file__).parent / "cloud-init.yaml.tpl"
target.write_text(content)
print("Wrote", len(content), "chars")
print()

# Verify key lines
print("=== VERIFICATION ===")
for i, line in enumerate(lines, 1):
    if "uri" in line and "try_files" in line:
        print(f"  L{i} (try_files): {line!r}")
    if "BRANCH=" in line and "1:-master" in line:
        print(f"  L{i} (BRANCH): {line!r}")
    if "server_name" in line:
        print(f"  L{i} (server_name): {line!r}")
    if "proxy_set_header Host" in line:
        print(f"  L{i} (Host header): {line!r}")
    if "%{" in line and ("if" in line or "endif" in line):
        print(f"  L{i} (conditional): {line!r}")
    if "certbot" in line.lower():
        print(f"  L{i} (certbot): {line!r}")