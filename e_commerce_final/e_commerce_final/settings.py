import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
ALLOWED_HOSTS = ['beautya.io.vn', 'www.beautya.io.vn']

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-fyrk4bhfj9r2*8^706005h4zo*e1=*t!$3dsx@@_ey4&$-6s%f"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv('GOOGLE_CLIENT_ID')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") 
OPENAI_API_KEY = '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' 


# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    'django.contrib.humanize',

    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    'social_django',
    "users.apps.UsersConfig",
    "products.apps.ProductsConfig",
    "orders.apps.OrdersConfig",
    "core.apps.CoreConfig",
    "blog.apps.BlogConfig",
]
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'users.pipeline.prevent_duplicate_google_linkage',
    'social_core.pipeline.social_auth.associate_user',
    
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "e_commerce_final.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates')],  # Dùng templates toàn cục
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                'core.context_processors.cart_item_count',
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",  
                "django.template.context_processors.static", 
            ],
        },
    },
]

WSGI_APPLICATION = "e_commerce_final.wsgi.application"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ✅ STATIC files (dùng chung cho toàn bộ project)
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]   # ✅ static nằm ở cấp project
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# ✅ MEDIA files (ảnh upload từ admin)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Allauth settings
SITE_ID = 1
LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = 'login'



AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',

]
SOCIAL_AUTH_AUTHENTICATION_ERROR_URL = '/oauth-error/'
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'optional'

AUTH_USER_MODEL = 'users.CustomUser'
