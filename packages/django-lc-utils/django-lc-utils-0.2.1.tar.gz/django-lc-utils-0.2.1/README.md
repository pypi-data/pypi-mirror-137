# Django LC Utils

Django app for various django utilities

`pip install django-lc-utils`

### Prerequisites

This package relies on `django-model-utils`, `Django`. 

## Running Tests

```
python manage.py test
```

## Usuage

In order to use the system you must add django_lc_utils to your installed apps in your settings.py file.

```python
INSTALLED_APPS = [
    'django_lc_utils'
]
```

## Utilities

1. Django Soft Delete Mixin

This is a custom mixin to enable soft delete feature on the Django models.

```python
from django_lc_utils.mixins import SoftDeleteMixin
from model_utils.models import TimeStampedModel

class TestModel(TimeStampedModel, SoftDeleteMixin):
    class Meta:
        db_table = "test_model"
        verbose_name = "Django Test Model"
        verbose_name_plural = "Djando Test Models"

    test_field = models.TextField("Test field")
```