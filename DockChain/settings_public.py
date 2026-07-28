"""
Settings for the public deploy of DockChain, mounted at /livesite/dockchain/
inside the shwetanshu-portfolio container (see that project's entrypoint.sh
and AWS/nginx config). Overrides the handful of dev-only values in
settings.py — DEBUG, SECRET_KEY, ALLOWED_HOSTS, the database (sqlite here
instead of the local MySQL dev setup, which also sidesteps shipping the
hardcoded MySQL password in settings.py), static file serving, and the
subpath mount itself (FORCE_SCRIPT_NAME/STATIC_URL/ROOT_URLCONF).
"""
import os

from .settings import *  # noqa: F401,F403

DEBUG = False

# settings.py never sets this at all — added here since is_secure()/request
# scheme detection matters behind the nginx proxy this app is mounted
# behind (see AWS/nginx/default.conf.template in the portfolio repo).
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SECRET_KEY = os.environ["DOCKCHAIN_SECRET_KEY"]

ALLOWED_HOSTS = [h.strip() for h in os.environ.get("DOCKCHAIN_ALLOWED_HOSTS", "").split(",") if h.strip()]

ROOT_URLCONF = "DockChain.public_urls"

# Mounted under this prefix by nginx — makes Django's own url reversal,
# request.path, and static() all resolve with the prefix included.
FORCE_SCRIPT_NAME = "/livesite/dockchain"
STATIC_URL = "/livesite/dockchain/static/"
STATIC_ROOT = BASE_DIR / "staticfiles_public"

# Inserted right after SecurityMiddleware, per whitenoise's own placement guidance.
MIDDLEWARE = [MIDDLEWARE[0], "whitenoise.middleware.WhiteNoiseMiddleware", *MIDDLEWARE[1:]]
# Plain (non-manifest) storage: the shared repo-root static/ dir covers every
# app, including ones excluded from this public deploy, and some of their
# CSS references broken image paths — CompressedManifestStaticFilesStorage
# fails collectstatic outright on any such reference anywhere in the tree.
# No cache-busting hashes as a result, but fine for this low-traffic demo.
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

# Reset every container boot — no persistence needed for this demo (see
# entrypoint.sh, which deletes this file before running migrate).
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db_public.sqlite3",
    }
}

CSRF_TRUSTED_ORIGINS = ["https://" + h for h in ALLOWED_HOSTS]
