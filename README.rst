.. _Python: https://www.python.org/
.. _Django: https://www.djangoproject.com/
.. _DjangoCMS: https://docs.django-cms.org/en/release-3.11.x/
.. _django-simple-captcha: https://django-simple-captcha.readthedocs.io/en/latest/
.. _django-phonenumber-field: https://django-phonenumber-field.readthedocs.io/en/latest/
.. _django-crispy-forms: https://django-crispy-forms.readthedocs.io/en/latest/
.. _crispy-bootstrap5: https://github.com/django-crispy-forms/crispy-bootstrap5

====================
emencia-request-form
====================

A simple contact form with some homemade antispam.

This application is a contact form that filters requests against specific criteria that
help prevent abusive spam.


Features
********

* Prevent some bot spams with some filtering criteria;
* DjangoCMS plugin to include form in pages;
* Use phonenumber library to check for correct phone number formats;
* Use Crispy forms to define form layout;


Dependencies
************

* `Python`_>=3.10;
* `Django`_>=4.0,<5.0;
* `DjangoCMS`_>=3.11.0,<4.0;
* `django-simple-captcha`_>=0.5.20,<1.0;
* `django-phonenumber-field`_>=7.2.0,<8.0;
* `django-crispy-forms`_>=2.0;
* `crispy-bootstrap5`_>=0.7;


Links
*****

* Read the documentation on `Read the docs <https://emencia-request-form.readthedocs.io/>`_;
* Download its `PyPi package <https://pypi.python.org/pypi/emencia-request-form>`_;
* Clone it on its `Github repository <https://github.com/emencia/emencia-request-form>`_;
