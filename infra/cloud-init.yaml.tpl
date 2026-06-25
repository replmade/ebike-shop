#cloud-config

package_update: true
package_upgrade: true

packages:
  - python3
  - python3-venv
  - python3-pip
  - nginx
  - git
  - certbot
  - python3-certbot-nginx

write_files:
  # --- Django production settings override ---
  - path: /opt/ebike-shop/.env
    owner: root:www-data
    permissions: "0640"
    content: |
      DJANGO_SECRET_KEY=${django_secret_key}
      DJANGO_ALLOWED_HOSTS=${domain != "" ? "${domain} www.${domain}" : "*"}
      DJANGO_DEBUG=False
      DJANGO_SETTINGS_MODULE=shop.settings

  # --- Gunicorn systemd unit ---
  - path: /etc/systemd/system/ebike-shop.service
    content: |
      [Unit]
      Description=ebike-shop Gunicorn daemon
      After=network.target

      [Service]
      User=www-data
      Group=www-data
      WorkingDirectory=/opt/ebike-shop/backend
      EnvironmentFile=/opt/ebike-shop/.env
      ExecStart=/opt/ebike-shop/backend/venv/bin/gunicorn \
          --workers 2 \
          --bind unix:/run/ebike-shop.sock \
          --timeout 120 \
          shop.wsgi:application
      Restart=always
      RestartSec=5

      [Install]
      WantedBy=multi-user.target

  # --- Nginx site config ---
  - path: /etc/nginx/sites-available/ebike-shop
    content: |
      server {
          listen 80;
          server_name ${domain != "" ? domain : "_"};

          location / {
              root /opt/ebike-shop/frontend/dist;
              try_files $$uri $$uri/ /index.html;
          }

          location /static/ {
              alias /opt/ebike-shop/backend/staticfiles/;
          }

          location /api/ {
              proxy_pass http://unix:/run/ebike-shop.sock;
              proxy_set_header Host $$host;
              proxy_set_header X-Real-IP $$remote_addr;
              proxy_set_header X-Forwarded-For $$proxy_add_x_forwarded_for;
              proxy_set_header X-Forwarded-Proto $$scheme;
          }

          location /admin/ {
              proxy_pass http://unix:/run/ebike-shop.sock;
              proxy_set_header Host $$host;
              proxy_set_header X-Real-IP $$remote_addr;
              proxy_set_header X-Forwarded-For $$proxy_add_x_forwarded_for;
              proxy_set_header X-Forwarded-Proto $$scheme;
          }
      }

  # --- Deploy script (also used for future updates) ---
  - path: /usr/local/bin/ebike-deploy
    permissions: "0755"
    content: |
      #!/usr/bin/env bash
      set -euo pipefail

      APP_DIR=/opt/ebike-shop
      BRANCH="$${1:-master}"

      echo "=== Pulling latest code (branch: $$BRANCH) ==="
      cd "$$APP_DIR"
      git fetch origin
      git checkout "$$BRANCH"
      git reset --hard "origin/$$BRANCH"

      echo "=== Setting up backend ==="
      cd "$$APP_DIR/backend"
      if [ ! -d venv ]; then
        python3 -m venv venv
      fi
      source venv/bin/activate
      pip install -r requirements.txt gunicorn
      python manage.py makemigrations api --noinput
      python manage.py migrate --noinput
      python manage.py collectstatic --noinput
      python manage.py seed_data || true

      echo "=== Setting up frontend ==="
      cd "$$APP_DIR/frontend"
      npm install
      npm run build

      echo "=== Restarting services ==="
      systemctl restart ebike-shop
      systemctl reload nginx

      echo "=== Deploy complete ==="

runcmd:
  # Clone the repo
  - git clone --branch "${repo_branch}" "${repo_url}" /opt/ebike-shop

  # Initial deploy
  - /usr/local/bin/ebike-deploy "${repo_branch}"

  # Create Django superuser via non-interactive manage.py
  - |
    cd /opt/ebike-shop/backend
    source venv/bin/activate
    DJANGO_SUPERUSER_PASSWORD="${django_superuser_password}" \
    DJANGO_SUPERUSER_EMAIL="${django_superuser_email}" \
    DJANGO_SUPERUSER_USERNAME="${django_superuser_email}" \
    python manage.py createsuperuser --noinput || true

  # Enable Gunicorn service
  - systemctl enable ebike-shop
  - systemctl start ebike-shop

  # Enable Nginx site
  - ln -sf /etc/nginx/sites-available/ebike-shop /etc/nginx/sites-enabled/ebike-shop
  - rm -f /etc/nginx/sites-enabled/default
  - systemctl reload nginx

  # Provision TLS if a domain is configured
${ if domain != "" }
  - certbot --nginx -n --agree-tos -m "${django_superuser_email}" -d "${domain}" || echo "TLS setup failed - configure DNS first, then run: certbot --nginx -d ${domain}"
${ endif }
