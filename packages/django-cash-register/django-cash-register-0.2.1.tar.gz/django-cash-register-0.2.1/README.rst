========================
DJANGO CASH REGISTER APP
========================

django-cash-register is a Django app to manage product by cashier.

Installation
============
::

    pip install django-cash-register

Quick start
===========

1. Add "django_cash_register" to your INSTALLED_APPS settings.py like this::

    INSTALLED_APPS = [
        ...
        'django_cash_register',
    ]

2. If you want to use django_cash_register as main url. Add "DJANGO_CASH_REGISTER_MAIN_PAGE" to settings.py like this::

    DJANGO_CASH_REGISTER_MAIN_PAGE = True

3. Add "STATICFILES_DIRS" to settings.py like this::

    STATICFILES_DIRS = [
        [BASE_DIR / 'static'][0]
    ]

4. Add "django_cash_register.urls" to urls.py like this::

    urlpatterns = [
        ...
        path('', include('django_cash_register.urls')),
    ]

5. Execute command::

    ./manage.py migrate

6. Start the development server and visit http://127.0.0.1:8000 or http://127.0.0.1:8000/django_cash_register

Application
===========

.. image:: https://user-images.githubusercontent.com/80222701/151967549-81e31bff-e9b3-48d4-926f-9f20a930449a.png