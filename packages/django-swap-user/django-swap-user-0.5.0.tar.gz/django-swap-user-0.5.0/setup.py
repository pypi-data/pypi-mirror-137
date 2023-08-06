# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['swap_user',
 'swap_user.tests',
 'swap_user.to_email',
 'swap_user.to_email.migrations',
 'swap_user.to_named_email',
 'swap_user.to_named_email.migrations',
 'swap_user.to_phone',
 'swap_user.to_phone.migrations',
 'swap_user.to_phone_otp',
 'swap_user.to_phone_otp.migrations']

package_data = \
{'': ['*']}

install_requires = \
['django-phonenumber-field[phonenumbers]>=5.2.0,<6.0.0', 'django>=2.2']

setup_kwargs = {
    'name': 'django-swap-user',
    'version': '0.5.0',
    'description': '(Beta) Simple and flexible way to swap default Django User',
    'long_description': '# Django-Swap-User (Beta)\n\n## About\nIf you are tired from copying one custom user model from one project to another ones - use this package.\nThis will do all for you. \n\n\n## Installation\n```\npip install django-swap-user\n```\n\n## Basic usage\n1. Choose one of models and settings from table:\n\n| Application name | Username field | Description                                                           | `INSTALLED_APPS`                                 | `AUTH_USER_MODEL`               |\n|------------------|----------------|-----------------------------------------------------------------------|------------------------------------------------|-----------------------------------|\n| `to_email`       | `email`        | User with `email` username                                            | ```"swap_user", "swap_user.to_email",```       | `"to_email.EmailUser"`            |\n| `to_named_email` | `email`        | User with `email` username, `first_name` and `last_name` extra fields | ```"swap_user", "swap_user.to_named_email",``` | `"to_named_email.NamedEmailUser"` |\n| `to_phone`       | `phone`        | User with `phone` username                                            | ```"swap_user", "swap_user.to_phone",```       | `"to_phone.PhoneUser"`            |\n| `to_phone_otp`   | `phone`        | User with `phone` username  and OTP authentication                    | ```"swap_user", "swap_user.to_phone_otp",```   | `"to_phone.PhoneOTPUser"`         |\n\n2. Add corresponding app to `INSTALLED_APPS`:\n```python\nINSTALLED_APPS = [\n    ...\n    "swap_user",\n    "swap_user.to_named_email",\n    ...\n]\n```\n3. Change `AUTH_USER_MODEL` to corresponding:\n```python\nAUTH_USER_MODEL = "to_named_email.NamedEmailUser"\n```\n\n\n## Architecture\nApplication `swap_user` split into 3 apps:\n  - `to_email` - provides user with `email` username field\n  - `to_named_email` - provides user with `email` username field and with `first_name`, `last_name` extra fields\n  - `to_phone` - provides user with `phone` username field\n  - `to_phone_otp` - provides user with `phone` username field and with OTP authentication\n  \n  \n## Why?\nBecause if we leave them in one app, they all will create migrations and tables - such approach leads us to redundant tables.\nThey will be treated as 3 custom models within the same app, which causes perplexing and cognitive burden.\n\nWith such approach (when there is a common app which contains internal apps) - the user \nchoose and connect only the specific user model which suits best for concrete business-logic. \n\nI have found such approach at Django REST Framework `authtoken` application and decide to use it - reference is [here](https://github.com/encode/django-rest-framework/tree/master/rest_framework/authtoken).\n',
    'author': 'Artem Innokentiev',
    'author_email': 'artinnok@protonmail.com',
    'maintainer': 'Artem Innokentiev',
    'maintainer_email': 'artinnok@protonmail.com',
    'url': 'http://github.com/artinnok/django-swap-user',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
