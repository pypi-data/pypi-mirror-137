from django.db.models import ManyToOneRel, OneToOneRel
from django.db import models
from model_utils.managers import QueryManager

class SoftDeleteMixin(models.Model):
    is_removed = models.BooleanField(default=False, editable=False)

    class Meta:
        abstract = True

    objects = QueryManager(is_removed=False)
    deleted = QueryManager(is_removed=True)
    all_objects = models.Manager()

    def delete(self, using=None, soft=True, *args, **kwargs):
        """
        Soft delete object (set its ``is_removed`` field to True).
        Actually delete object if setting ``soft`` to False.
        """
        if soft:
            self.is_removed = True
            self.save(using=using)
        else:
            return super().delete(using=using, *args, **kwargs)