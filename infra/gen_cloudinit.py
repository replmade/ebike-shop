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

def lit(var):
    return DS + DS + var

# Variable names stored as plain strings (no dollar-brace in source)
SK = "django_secret_key"
PW = "django_superuser_password"
EM = "django_superuser_email"
RB = "repo_branch"
RU = "repo_url"
DM = "domain"

lines = []
L = lines.append

L("#cloud-config"); L(""); L("package_update: true"); L("package_upgrade: true"); L("")
L("packages:")
for p in ["python3","python3-venv","python3-pip","nginx","git","certbot","python3-certbot-nginx"]:
    L("  - " + p)
L("")

L("write_files:")
L("  # --- Django production settings override ---")
L("  - path: /opt/ebike-shop/.env")
L("    owner: root:www-data")
L("    permissions: " + Q + "0640" + Q)
L("    content: |")
L("      DJANGO_SECRET_KEY=" + DS + OB + SK + CB)
L("      DJANGO_ALLOWED_HOSTS=" + DS+OB + "domain != " + Q+Q + " ? " + Q + tf(DM) + " www." + tf(DM) + Q + " : " + Q + "*" + Q + DS+CB)
L("      DJANGO_DEBUG=False")
L("      DJANGO_SETTINGS_MODULE=shop.settings")
L("")

L("  # --- Gunicorn systemd unit ---")
L("  - path: /etc/systemd/system/ebike-shop.service")
L("    content: |")
L("      [Unit]"); L("      Description=ebike-shop Gunicorn daemon"); L("      After=network.target"); L("")
L("      [Service]"); L("      User=www-data"); L("      Group=www-data")
L("      WorkingDirectory=/opt/ebike-shop/backend")
L("      EnvironmentFile=/opt/ebike-shop/.env")
L("      ExecStart=/opt/ebike-shop/backend/venv/bin/gunicorn " + BS)
L("          --workers 2 " + BS); L("          --bind unix:/run/ebike-shop.sock " + BS)
L("          --timeout 120 " + BS); L("          shop.wsgi:application")
L("      Restart=always"); L("      RestartSec=5"); L("")
L("      [Install]"); L("      WantedBy=multi-user.target"); L("")

L("  # --- Nginx site config ---")
L("  - path: /etc/nginx/sites-available/ebike-shop")
L("    content: |")
L("      server {"); L("          listen 80;")
L("          server_name " + DS+OB + "domain != " + Q+Q + " ? domain : " + Q + "_" + Q + DS+CB + ";")
L(""); L("          location / {"); L("              root /opt/ebike-shop/frontend/dist;")
L("              try_files " + lit("uri") + " " + lit("uri") + "/ /index.html;"); L("          }"); L("")
L("          location /static/ {"); L("              alias /opt/ebike-shop/backend/staticfiles/;"); L("          }"); L("")
L("          location /api/ {"); L("              proxy_pass http://unix:/run/ebike-shop.sock;")
L("              proxy_set_header Host " + lit("host") + ";")
L("              proxy_set_header X-Real-IP " + lit("remote_addr") + ";")
L("              proxy_set_header X-Forwarded-For " + lit("proxy_add_x_forwarded_for") + ";")
L("              proxy_set_header X-Forwarded-Proto " + lit("scheme") + ";"); L("          }"); L("")
L("          location /admin/ {"); L("              proxy_pass http://unix:/run/ebike-shop.sock;")
L("              proxy_set_header Host " + lit("host") + ";")
L("              proxy_set_header X-Real-IP " + lit("remote_addr") + ";")
L("              proxy_set_header X-Forwarded-For " + lit("proxy_add_x_forwarded_for") + ";")
L("              proxy_set_header X-Forwarded-Proto " + lit("scheme") + ";"); L("          }"); L("      }"); L("")

L("  # --- Deploy script (also used for future updates) ---")
L("  - path: /usr/local/bin/ebike-deploy")
L("    permissions: " + Q + "0755" + Q)
L("    content: |")
L("      #!/usr/bin/env bash"); L("      set -euo pipefail"); L("")
L("      APP_DIR=/opt/ebike-shop")
L("      BRANCH=" + Q + lit("{1:-master") + ")" + Q); L("")
L("      echo " + Q + "=== Pulling latest code (branch: " + lit("BRANCH") + ") ===" + Q)
L("      cd " + Q + lit("APP_DIR") + Q); L("      git fetch origin")
L("      git checkout " + Q + lit("BRANCH") + Q)
L("      git reset --hard " + Q + "origin/" + lit("BRANCH") + Q); L("")
L("      echo " + Q + "=== Setting up backend ===" + Q)
L("      cd " + Q + lit("APP_DIR") + "/backend" + Q)
L("      if [ ! -d venv ]; then"); L("        python3 -m venv venv"); L("      fi")
L("      source venv/bin/activate"); L("      pip install -r requirements.txt gunicorn")
L("      python manage.py makemigrations api --noinput")
L("      python manage.py migrate --noinput")
L("      python manage.py collectstatic --noinput")
L("      python manage.py seed_data || true"); L("")
L("      echo " + Q + "=== Setting up frontend ===" + Q)
L("      cd " + Q + lit("APP_DIR") + "/frontend" + Q)
L("      npm install"); L("      npm run build"); L("")
L("      echo " + Q + "=== Restarting services ===" + Q)
L("      systemctl restart ebike-shop"); L("      systemctl reload nginx"); L("")
L("      echo " + Q + "=== Deploy complete ===" + Q); L("")

L("runcmd:")
L("  # Clone the repo")
L("  - git clone --branch " + Q + tf(RB) + Q + " " + Q + tf(RU) + Q + " /opt/ebike-shop"); L("")
L("  # Initial deploy")
L("  - /usr/local/bin/ebike-deploy " + Q + tf(RB) + Q); L("")
L("  # Create Django superuser via non-interactive manage.py")
L("  - |"); L("    cd /opt/ebike-shop/backend"); L("    source venv/bin/activate")
L("    DJANGO_SUPERUSER_PASSWORD=" + Q + DS + OB + PW + CB + Q + " " + BS)
L("    DJANGO_SUPERUSER_EMAIL=" + Q + tf(EM) + Q + " " + BS)
L("    DJANGO_SUPERUSER_USERNAME=" + Q + tf(EM) + Q + " " + BS)
L("    python manage.py createsuperuser --noinput || true"); L("")
L("  # Enable Gunicorn service")
L("  - systemctl enable ebike-shop"); L("  - systemctl start ebike-shop"); L("")
L("  # Enable Nginx site")
L("  - ln -sf /etc/nginx/sites-available/ebike-shop /etc/nginx/sites-enabled/ebike-shop")
L("  - rm -f /etc/nginx/sites-enabled/default"); L("  - systemctl reload nginx"); L("")
L("  # Provision TLS if a domain is configured")
L("%" + DS+OB + " if domain != " + Q+Q + " " + CB)
L("  - certbot --nginx -n --agree-tos -m " + Q + tf(EM) + Q + " -d " + Q + tf(DM) + Q)
L("%" + DS+OB + " endif " + CB)

content = "\n".join(lines) + "\n"
target = pathlib.Path("/Users/c/github/ebike-shop/infra/cloud-init.yaml.tpl")
target.write_text(content)
print("Wrote", len(content), "chars")
for i, line in enumerate(lines, 1):
    if "SECRET_KEY" in line or "SUPERUSER_PASSWORD" in line or "server_name" in line or "certbot" in line or ("%" in line and "if" in line) or ("%" in line and "endif" in line):
        print(f"  L{i}: {repr(line)}")