"""
Django settings for yahoonews project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os



# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'zqyh_qotqegj4khxgnrvytfdw#2-@i%#od497h%is$t+gc#tgq'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django_crontab',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'news'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
ROOT_URLCONF = 'yahoonews.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR+"/templates"],
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

WSGI_APPLICATION = 'yahoonews.wsgi.application'



# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.postgresql',
        # 'NAME': 'yahoo',
        # 'USER': 'dbyang',
        # 'PASSWORD': 'pg@1989',
        # 'HOST': '127.0.0.1',
        # 'PORT': '5432',
        
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test',
        'USER': 'root',
        'PASSWORD': '123',
        'HOST':'localhost',
        'PORT':'3306',
        'TEST': {
                'CHARSET': 'utf8',
                'COLLATION': 'utf8_general_ci',
            }
        #'ENGINE': None
    }
}



# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = BASE_DIR+'/static/'

# 定时任务
CRONJOBS = [
    ('*/1 * * * *', 'news.views.auto_task','>>'+BASE_DIR+'/log/crontab_log.log')
]


LOGGING = {
    'version': 1,  # 保留字
    'disable_existing_loggers': False,  # 禁用已经存在的logger实例
    # 日志文件的格式
    'formatters': {
        # 详细的日志格式
        'standard': {
            'format': '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]'
                      '[%(levelname)s][%(message)s]'
        },
        # 简单的日志格式
        'simple': {
            'format': '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
        },
        # 定义一个特殊的日志格式
        'collect': {
            'format': '%(message)s'
        }
    },
    # 过滤器
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    # 处理器
    'handlers': {
        # 在终端打印
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],  # 只有在Django debug为True时才在屏幕打印日志
            'class': 'logging.StreamHandler',  #
            'formatter': 'simple'
        },
        # 默认的
        # 'default': {
        #     'level': 'INFO',
        #     'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
        #     'filename': os.path.join(BASE_LOG_DIR, "xxx_info.log"),  # 日志文件
        #     'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
        #     'backupCount': 3,  # 最多备份几个
        #     'formatter': 'standard',
        #     'encoding': 'utf-8',
        # },
        # 专门用来记错误日志
        # 'error': {
        #     'level': 'ERROR',
        #     'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
        #     'filename': os.path.join(BASE_LOG_DIR, "xxx_err.log"),  # 日志文件
        #     'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
        #     'backupCount': 5,
        #     'formatter': 'standard',
        #     'encoding': 'utf-8',
        # },
        # 专门定义一个收集特定信息的日志
        # 'collect': {
        #     'level': 'INFO',
        #     'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
        #     'filename': os.path.join(BASE_LOG_DIR, "xxx_collect.log"),
        #     'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
        #     'backupCount': 5,
        #     'formatter': 'collect',
        #     'encoding': "utf-8"
        # }
    },
    'loggers': {
       # 默认的logger应用如下配置
        '': {
            'handlers': ['console'],  # 上线之后可以把'console'移除
            'level': 'DEBUG',
            'propagate': True,  # 向不向更高级别的logger传递
        },
        # 名为 'collect'的logger还单独处理
        # 'collect': {
        #     'handlers': ['console', 'collect'],
        #     'level': 'INFO',
        # }
    },
}