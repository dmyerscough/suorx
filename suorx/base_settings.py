"""
Django settings for suorx project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

PRODUCTION = True

if PRODUCTION:
    from prod_settings import *
else:
    from dev_settings import *
