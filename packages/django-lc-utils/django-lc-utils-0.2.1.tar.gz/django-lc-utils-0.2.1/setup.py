# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_lc_utils', 'django_lc_utils.migrations']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.1.13,<4.0.0', 'django-model-utils>=4.2.0,<5.0.0']

setup_kwargs = {
    'name': 'django-lc-utils',
    'version': '0.2.1',
    'description': 'Utilities for Django application',
    'long_description': '# Django LC Utils\n\nDjango app for various django utilities\n\n`pip install django-lc-utils`\n\n### Prerequisites\n\nThis package relies on `django-model-utils`, `Django`. \n\n## Running Tests\n\n```\npython manage.py test\n```\n\n## Usuage\n\nIn order to use the system you must add django_lc_utils to your installed apps in your settings.py file.\n\n```python\nINSTALLED_APPS = [\n    \'django_lc_utils\'\n]\n```\n\n## Utilities\n\n1. Django Soft Delete Mixin\n\nThis is a custom mixin to enable soft delete feature on the Django models.\n\n```python\nfrom django_lc_utils.mixins import SoftDeleteMixin\nfrom model_utils.models import TimeStampedModel\n\nclass TestModel(TimeStampedModel, SoftDeleteMixin):\n    class Meta:\n        db_table = "test_model"\n        verbose_name = "Django Test Model"\n        verbose_name_plural = "Djando Test Models"\n\n    test_field = models.TextField("Test field")\n```',
    'author': 'Tejas Bhandari',
    'author_email': 'tejas@thesummitgrp.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Lenders-Cooperative/django-lc-utils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
