"""
Django settings for music_manage project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
from datetime import timedelta
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure--w0sv+_2@9y635y9kol)73n!70-e%-p)^+%8hlm%7w6vz$oh4$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'music.apps.MusicConfig',
    'django_json_widget',
    'drf_spectacular',

    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'dj_rest_auth'


]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'music.middleware.AccessTokenMiddleware',
]

ROOT_URLCONF = 'music_manage.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'music_manage.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }

    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "music-pro",
        "USER": "root",
        "PASSWORD": "12345678",
        "HOST": "127.0.0.1",
        "PORT": "3306",
        'OPTIONS': {
            'charset': 'utf8mb4',  # 支持存储包括表情符号在内的完整UTF-8字符集
        },
    }

}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    # ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',  # 设置 drf-spectacular 的 schema class






}





SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# dj-rest-auth
REST_AUTH = {
    "USE_JWT": True,
    # "JWT_AUTH_COOKIE": "_auth",  # Don't send access token cookie
    # "JWT_AUTH_REFRESH_COOKIE": "_refresh", # Don't send refresh token cookie
    "JWT_AUTH_HTTPONLY": False,  # Makes sure refresh token is sent
}

REST_USE_JWT = True

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/




STATIC_URL = "/static/"

STATIC_ROOT = os.path.join(BASE_DIR, "static")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "staticfiles"),
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# settings.py

# SPECTACULAR_SETTINGS = {
#     'TITLE': 'Your API',
#     'DESCRIPTION': 'Test description',
#     'VERSION': '1.0.0',
#     'SERVE_INCLUDE_SCHEMA': False,  # 不需要显示 schema 页面
#     'SECURITY': [{'BearerAuth': []}],  # 配置安全定义
#     'SECURITY_DEFINITIONS': {
#         'BearerAuth': {
#             'type': 'http',
#             'scheme': 'bearer',
#             'bearerFormat': 'JWT',
#         },
#     },
# }
SPECTACULAR_SETTINGS = {
    'TITLE': 'Your API Title',
    'DESCRIPTION': 'Detailed description of your API',
    'VERSION': '1.0.0',

    # 配置自定义的认证方式
    'SECURITY': [
        {'BearerAuth': []},  # 自定义认证的名称
    ],

    # 定义认证方案
    'SECURITY_SCHEMES': {
        'BearerAuth': {  # 自定义认证名称
            'type': 'http',
            'scheme': 'bearer',  # 使用 Bearer 作为认证类型
            'bearerFormat': 'JWT',  # 可以选择 'Token' 或 'JWT'
            'description': 'Enter your JWT access token to access secured endpoints.',
        },
    },

    'SWAGGER_UI_SETTINGS': {
        'persistAuthorization': True,  # 保持授权信息
        'deepLinking': True,
    },

    # 其他设置...
}




# SPECTACULAR_SETTINGS = {
#     'TITLE': '你的API文档标题',
#     'DESCRIPTION': '详细描述你的API文档的内容',
#     'VERSION': '1.0.0',
#     'SERVE_INCLUDE_SCHEMA': False,
#
#     # 配置认证方式
#     'SECURITY': [
#         {'jwtAuth': []},  # JWT 或其他自定义认证类型
#     ],
#
#     # 其他设置
#     'SWAGGER_UI_SETTINGS': {
#         'persistAuthorization': True,
#     },
#     'SWAGGER_UI_OAUTH_CONFIG': {
#         'clientId': 'your-client-id',
#         'clientSecret': 'your-client-secret',
#         'scopes': 'openid profile email',
#     },
#     'COMPONENT_SPLIT_REQUEST': True,  # 更详细的请求 schema 分离
#
#
# }