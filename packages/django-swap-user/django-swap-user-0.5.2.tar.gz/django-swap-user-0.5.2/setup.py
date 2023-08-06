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
    'version': '0.5.2',
    'description': '(Beta) Simple and flexible way to swap default Django User',
    'long_description': '# Django-Swap-User (Beta)\n\n## About\nIf you are tired from copying one custom user model from one project to another ones - use this package.\nThis will do all for you. \n\n\n## Installation\n```\npip install django-swap-user\n```\n\n## Basic usage\n1. Choose one of models that suits for you and copy related settings from the table:\n\n| Application name      | Username field | Description                                                           | `INSTALLED_APPS`                               | `AUTH_USER_MODEL`                      |\n|-----------------------|----------------|-----------------------------------------------------------------------|------------------------------------------------|----------------------------------------|\n| `swap_to_email`       | `email`        | User with `email` username                                            | ```"swap_user", "swap_user.to_email",```       | `"to_email.swap_to_email"`             |\n| `swap_to_named_email` | `email`        | User with `email` username, `first_name` and `last_name` extra fields | ```"swap_user", "swap_user.to_named_email",``` | `"swap_to_named_email.NamedEmailUser"` |\n| `swap_to_phone`       | `phone`        | User with `phone` username                                            | ```"swap_user", "swap_user.to_phone",```       | `"swap_to_phone.PhoneUser"`            |\n| `swap_to_phone_otp`   | `phone`        | User with `phone` username  and OTP authentication                    | ```"swap_user", "swap_user.to_phone_otp",```   | `"swap_to_phone_otp.PhoneOTPUser"`     |\n\n2. Add corresponding app to `INSTALLED_APPS`:\n```python\nINSTALLED_APPS = [\n    ...\n    "swap_user",\n    "swap_user.to_named_email",\n    ...\n]\n```\n3. Change `AUTH_USER_MODEL` to corresponding:\n```python\nAUTH_USER_MODEL = "swap_to_named_email.NamedEmailUser"\n```\n\n4. Apply migrations:\n```bash\npython manage.py migrate swap_to_named_email\n```\n\n\n## Architecture\nApplication `swap_user` split into 3 apps:\n  - `to_email` - provides user with `email` username field\n  - `to_named_email` - provides user with `email` username field and with `first_name`, `last_name` extra fields\n  - `to_phone` - provides user with `phone` username field\n  - `to_phone_otp` - provides user with `phone` username field and with OTP authentication\n  \n  \n## Why so unusual architecture?\nBecause if we leave them in one app, they all will create migrations and tables - such approach leads us to redundant tables.\nThey will be treated as 3 custom models within the same app, which causes perplexing and cognitive burden.\n\nWith such approach (when there is a common app which contains internal apps) - the user \nchoose and connect only the specific user model which suits best for concrete business-logic. \n\nI have found such approach at Django REST Framework `authtoken` application and decide to use it - reference is [here](https://github.com/encode/django-rest-framework/tree/master/rest_framework/authtoken).\n\n\n## Providing User model at start of project\nWhen you are starting a project from zero or scratch - this is a best moment to provide custom User model.\nBecause you have\'t a lot of migrations or you can easily regenerate them. Moreover, Django\'s [official docs](https://docs.djangoproject.com/en/dev/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project)\nrecommend to provide custom User model even if you are fully satisfied with default one - in future it will be easier to extend custom model that fits into your business cases.\n\n\n## Providing User model at mid of project\nThis is a harder way of doing things, but it is still possible to do:\n- Do all the steps at testing database and ONLY IF all of them was successful - try to apply at production environment\n- Please note that these steps are **common** - they fit in most cases, but in some circumstances you need act on situation.\n- Create a backup of your database\n- Add stable tag into your repository or save a commit hash reference\n- Pray to the heavens\n- Remove all of yours migrations in every app of Django\'s project\n- Remove all records from `django_migrations` table, for example with SQL `TRUNCATE django_migrations`\n- Now we have a "clean" state, so we can change default model\n- Generate new migrations for all of your applications - `python manage.py makemigrations` \n- Now we need to [fake migrate](https://docs.djangoproject.com/en/4.0/ref/django-admin/#cmdoption-migrate-fake) because we already have all the tables with data\n- First fake the `auth` application because we are depending from this one - `python manage.py migrate --fake auth`\n- Install this library, follow instructions and apply migrations\n- Then fake rest of migrations we have - `python manage.py migrate --fake`\n- Run your application!',
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
