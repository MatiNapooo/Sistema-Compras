import os
from pathlib import Path
import dj_database_url

# 1. Definición de rutas
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. Seguridad
SECRET_KEY = 'django-insecure-NextPrintSecreto'
DEBUG = True
ALLOWED_HOSTS = ['*']

# 3. Apps Instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary_storage',           # <-- DEBE ir ANTES de staticfiles
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'cloudinary',
    'core',
]

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

ROOT_URLCONF = 'compras_project.urls'

# 4. Templates
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

WSGI_APPLICATION = 'compras_project.wsgi.application'

# 5. Base de Datos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Si estamos en Heroku, sobreescribimos la base de datos:
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

# 6. Idioma y Zona Horaria
LANGUAGE_CODE = 'es-ar'
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_I18N = True
USE_TZ = True
USE_THOUSAND_SEPARATOR = True
DECIMAL_SEPARATOR = ','
THOUSAND_SEPARATOR = '.'
NUMBER_GROUPING = 3

# 7. Archivos Estáticos
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# 8. Archivos Multimedia
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 9. Cloudinary (almacenamiento de imágenes de perfil en la nube)
import cloudinary

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME', 'dvinasjl9'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY', '331969733158713'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET', '4-ACWlJhFEq351-TYPbi9IRYoeM'),
}

# Configurar cloudinary SDK directamente (necesario para que .url funcione)
cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME', 'dvinasjl9'),
    api_key=os.environ.get('CLOUDINARY_API_KEY', '331969733158713'),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET', '4-ACWlJhFEq351-TYPbi9IRYoeM'),
    secure=True
)

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'