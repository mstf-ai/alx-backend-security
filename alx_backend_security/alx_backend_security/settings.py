import os
from pathlib import Path

# =========================================
# 🏗️ الأساسيات العامة
# =========================================

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-change-this-key'  # غيّرها قبل الإنتاج

DEBUG = True

ALLOWED_HOSTS = ['*']  # أثناء التطوير فقط


# =========================================
# ⚙️ التطبيقات المثبتة
# =========================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ip_tracking',         # تطبيق تتبع الـ IP
    'django_ratelimit',    # مكتبة rate limiting
]


# =========================================
# ⚙️ Middleware
# =========================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # 🧩 ميدلوير تسجيل وتتبع الـ IPs
    'ip_tracking.middleware.IPLoggingMiddleware',
]


# =========================================
# ⚙️ إعدادات الجذر والتوجيه
# =========================================

ROOT_URLCONF = 'alx_backend_security.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'alx_backend_security.wsgi.application'


# =========================================
# ⚙️ قاعدة البيانات
# =========================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# =========================================
# ⚙️ كلمة السر والتحقق
# =========================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# =========================================
# 🌍 اللغة والمنطقة الزمنية
# =========================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Cairo'
USE_I18N = True
USE_TZ = True


# =========================================
# 📁 الملفات الثابتة
# =========================================

STATIC_URL = 'static/'


# =========================================
# 💾 نظام الكاش للتطوير المحلي (LocMemCache)
# =========================================

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}


# =========================================
# 🟢 إعدادات rate limiting (مؤقت بدون Redis)
# =========================================

RATELIMIT_ENABLE = False   # مؤقتًا لتجنب مشاكل LocMemCache
RATELIMIT_USE_CACHE = "default"


# =========================================
# ✅ إعدادات إضافية
# =========================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
