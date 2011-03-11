DEBUG = True

# for a list of backends see
# http://docs.djangoproject.com/en/1.2/ref/settings/#std:setting-ENGINE

DATABASES = {
    'default': {
        'ENGINE':    'django.db.backends.mysql',
        'NAME':      'conlot',
        'USER':      'conlot',
        'PASSWORD':  'conlot',
        'HOST':      '',
        'PORT':      '',
    }
}


