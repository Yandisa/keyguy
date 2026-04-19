# KeyGuy Boss D — Django Website

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create database tables
python manage.py migrate

# 3. Load all initial content (services, areas, FAQs, reviews, settings)
python manage.py loaddata core/fixtures/initial_data.json

# 4. Create your admin login
python manage.py createsuperuser

# 5. Run the development server
python manage.py runserver
```

Then open:
- **Website:** http://127.0.0.1:8000/
- **Admin:** http://127.0.0.1:8000/admin/

---

## What the Admin Can Change

Log in at `/admin/` and you can edit everything without touching code:

| Section | What you can change |
|---|---|
| **Site Settings** | Business name, both phone numbers, WhatsApp, email, hero text, hero image, stats, SEO |
| **Services** | Add/remove/reorder services, change icons and descriptions |
| **Testimonials** | Add real customer reviews, set ratings, reorder |
| **Service Areas** | Add/remove areas covered |
| **FAQs** | Add/edit/reorder questions and answers |
| **Gallery** | Upload photos or paste image URLs |
| **Quote Requests** | View all enquiries from the website form, mark status (New / Contacted / Completed) |

---

## Customer Changes Applied

From the WhatsApp conversation (18 April 2025):
- ✅ Business name updated to **KeyGuy Boss D**
- ✅ Primary phone: **084 815 7329**
- ✅ Secondary phone: **076 827 4530** (both shown in topbar and contact section)
- ✅ **Mobile Diagnostics** added as a service

---

## Production Checklist

Before going live:
1. Set `DEBUG = False` in `keyguy/settings.py`
2. Set a real `SECRET_KEY`
3. Add your domain to `ALLOWED_HOSTS`
4. Configure email in settings (SMTP details)
5. Run `python manage.py collectstatic`
6. Use gunicorn + nginx or deploy to Railway / Render / PythonAnywhere

---

## Project Structure

```
keyguy/
├── manage.py
├── requirements.txt
├── keyguy/          ← project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── core/            ← main app
    ├── models.py    ← all content models
    ├── admin.py     ← admin configuration
    ├── views.py     ← homepage view
    ├── forms.py     ← quote request form
    ├── context_processors.py
    ├── fixtures/
    │   └── initial_data.json   ← seed data
    └── templates/core/
        └── home.html           ← the full website template
```
