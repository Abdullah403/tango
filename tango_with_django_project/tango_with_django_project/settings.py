"""
Django settings for tango_with_django_project project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))



# Quick-start development settings - unsuitable for production

# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&$a&w93c!2x%7mat)@r&l*y_l0e407@dg)io9164a8m3oipwv('

# SECURITY WARNING: don't run with debug turned on in production!
SITE_ID = 1
DEBUG = True

TEMPLATE_DEBUG = True

TEMPLATE_DIRS = (
      os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/'),
     )




STATICFILES_DIRS=(
       os.path.join(os.path.dirname(__file__), 'static').replace('\\','/'),
                  )

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media').replace('\\','/')





ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.auth', # THIS LINE SHOULD BE PRESENT AND UNCOMMENTED
    'django.contrib.contenttypes', # THIS LINE SHOULD BE PRESENT AND UNCOMMENTED
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
   
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'rango',
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'tango_with_django_project.urls'

WSGI_APPLICATION = 'tango_with_django_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'rango.db'),
    }
}

DATABASE_PATH = os.path.join(BASE_DIR, 'rango.db')

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
SESSION_EXPIRE_AT_BROWSER_CLOSE=False
SESSION_COOKIE_AGE = 1209600




# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
