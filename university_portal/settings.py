import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv

# ==================== ENVIRONMENT LOADING ====================
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env', override=True)

# Verify critical variables immediately
required_vars = [
    'SECRET_KEY',
    'CLOUDINARY_CLOUD_NAME',
    'CLOUDINARY_API_KEY',
    'CLOUDINARY_API_SECRET'
]
missing = [var for var in required_vars if not os.environ.get(var)]
if missing:
    raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")

# ==================== CORE SETTINGS ====================
SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = os.environ.get('DEBUG', '0') == '1'

ALLOWED_HOSTS = ['localhost', '127.0.0.1']
if RENDER_EXTERNAL_HOSTNAME := os.environ.get('RENDER_EXTERNAL_HOSTNAME'):
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Security
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# ==================== APPLICATIONS ====================
INSTALLED_APPS = [
    # Cloudinary apps in correct order
    'cloudinary_storage',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary',
    'django.contrib.staticfiles',
    
    # Local apps
    'accounts',
    'departments',
    'posts',
    'messaging',
    'results',
    
    # Third-party
    'crispy_forms',
    'crispy_bootstrap5',
    'django_filters',
    'channels',
]

# ==================== MIDDLEWARE ====================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ==================== TEMPLATES & URLs ====================
ROOT_URLCONF = 'university_portal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ==================== DATABASE ====================
DATABASES = {
    'default': dj_database_url.config(
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# ==================== AUTHENTICATION ====================
AUTH_USER_MODEL = 'accounts.User'
LOGIN_REDIRECT_URL = 'home'
LOGIN_URL = 'login'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ==================== INTERNATIONALIZATION ====================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ==================== STATIC FILES ====================
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ==================== MEDIA FILES (CLOUDINARY) ====================
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
MEDIA_URL = '/media/'  # For URL reverse compatibility

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ['CLOUDINARY_CLOUD_NAME'],
    'API_KEY': os.environ['CLOUDINARY_API_KEY'],
    'API_SECRET': os.environ['CLOUDINARY_API_SECRET'],
    'SECURE': True,
    'EXCLUDE_DELETE_ORPHANED_MEDIA': True,
    'STATICFILES_MANIFEST_ROOT': os.path.join(BASE_DIR, 'manifest'),
}

# Initialize Cloudinary SDK
import cloudinary
cloudinary.config(
    cloud_name=os.environ['CLOUDINARY_CLOUD_NAME'],
    api_key=os.environ['CLOUDINARY_API_KEY'],
    api_secret=os.environ['CLOUDINARY_API_SECRET'],
    secure=True
)

# ==================== CUSTOM STORAGE FOR NON-IMAGE FILES ====================
from cloudinary_storage.storage import MediaCloudinaryStorage

class CustomCloudinaryStorage(MediaCloudinaryStorage):
    def _upload(self, name, content, **kwargs):
        # Force 'raw' for non-image files
        if not any(name.lower().endswith(ext) for ext in ('.png', '.jpg', '.jpeg', '.gif', '.webp')):
            kwargs.update({'resource_type': 'raw'})
        return super()._upload(name, content, **kwargs)

DEFAULT_FILE_STORAGE = 'university_portal.settings.CustomCloudinaryStorage'

# ==================== WSGI/ASGI ====================
WSGI_APPLICATION = 'university_portal.wsgi.application'
ASGI_APPLICATION = "university_portal.asgi.application"

# ==================== OTHER SETTINGS ====================
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'