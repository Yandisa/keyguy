# Deploying KeyGuy Boss D to Coolify via GitHub

## 1. Push to GitHub

```bash
cd keyguy
git init
git add .
git commit -m "Initial commit — KeyGuy Boss D"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/keyguy.git
git push -u origin main
```

---

## 2. Connect GitHub to Coolify

1. Log into your Coolify dashboard
2. Go to **Sources** → Add GitHub
3. Authorise Coolify to access your repository

---

## 3. Create the App in Coolify

1. Click **New Resource** → **Application**
2. Choose your GitHub repo (`keyguy`)
3. Set branch: `main`
4. Build pack: **Dockerfile** (Coolify detects it automatically)
5. Port: `8000`

---

## 4. Set Environment Variables

In Coolify → your app → **Environment Variables**, add:

| Variable | Value |
|---|---|
| `SECRET_KEY` | A long random string (generate one below) |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `yourdomain.com,www.yourdomain.com` |
| `CSRF_TRUSTED_ORIGINS` | `https://yourdomain.com,https://www.yourdomain.com` |
| `DJANGO_SUPERUSER_USERNAME` | `admin` |
| `DJANGO_SUPERUSER_EMAIL` | `keyesdiagnosis@gmail.com` |
| `DJANGO_SUPERUSER_PASSWORD` | A strong password |

**Generate a SECRET_KEY** (run this on your local machine):
```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

**Email variables (optional — for quote notifications):**

| Variable | Value |
|---|---|
| `EMAIL_BACKEND` | `django.core.mail.backends.smtp.EmailBackend` |
| `EMAIL_HOST` | `smtp.gmail.com` |
| `EMAIL_PORT` | `587` |
| `EMAIL_USE_TLS` | `True` |
| `EMAIL_HOST_USER` | `keyesdiagnosis@gmail.com` |
| `EMAIL_HOST_PASSWORD` | Your Gmail App Password |

> To get a Gmail App Password: Google Account → Security → 2-Step Verification → App Passwords

---

## 5. Add Persistent Storage (important for SQLite + media)

In Coolify → your app → **Storages**, add two volumes:

| Container path | Description |
|---|---|
| `/app/db.sqlite3` | Database file |
| `/app/media` | Uploaded images |

This keeps your data safe across deployments.

---

## 6. Deploy

Click **Deploy** in Coolify. It will:
- Pull from GitHub
- Build the Docker image
- Run `startup.sh` which:
  - Runs database migrations
  - Loads initial data (services, areas, FAQs etc.)
  - Creates the admin superuser
  - Starts gunicorn

---

## 7. Set up your Domain

In Coolify → your app → **Domains**:
- Add `yourdomain.com`
- Enable **HTTPS** (Coolify handles the SSL certificate automatically via Let's Encrypt)

---

## 8. Access the Admin

Go to `https://yourdomain.com/admin/`

Log in with the username and password you set in environment variables.

From the admin you can edit:
- **Site Settings** — business name, phones, hero text, images
- **Services** — add/remove/reorder
- **Testimonials** — add real customer reviews
- **Gallery** — upload your own photos
- **FAQs** — edit questions and answers
- **Quote Requests** — view all enquiries from the website form

---

## Updating the site

Just push to GitHub:
```bash
git add .
git commit -m "Update services"
git push
```

Coolify auto-deploys on every push to `main`.
