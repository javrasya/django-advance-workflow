import sys

from django.db import models, IntegrityError, transaction
from django.utils import six


__author__ = 'ahmetdal'


class BaseModelManager(models.Manager):
    def update_or_create(self, **kwargs):

        defaults = kwargs.pop('defaults', {})
        lookup = kwargs.copy()
        for f in self.model._meta.fields:
            if f.attname in lookup:
                lookup[f.name] = lookup.pop(f.attname)

        try:
            self._for_write = True
            obj = self.get(**lookup)
            sid = transaction.savepoint(using=self.db)
            for key, value in defaults.iteritems():
                setattr(obj, key, value)
            obj.save()
            transaction.savepoint_commit(sid, using=self.db)
            return obj, True
        except self.model.DoesNotExist:
            try:
                params = dict([(k, v) for k, v in kwargs.items() if '__' not in k])
                params.update(defaults)
                obj = self.model(**params)
                sid = transaction.savepoint(using=self.db)
                for key, value in params.iteritems():
                    setattr(obj, key, value)
                obj.save(force_insert=True, using=self.db)
                transaction.savepoint_commit(sid, using=self.db)
                return obj, True
            except IntegrityError as e:
                transaction.savepoint_rollback(sid, using=self.db)
                exc_info = sys.exc_info()
                try:
                    return self.get(**lookup), False
                except self.model.DoesNotExist:
                    # Re-raise the IntegrityError with its original traceback.
                    six.reraise(*exc_info)

    def get_object_or_None(self, **kwargs):

        try:
            return self.model.objects.get(**kwargs)
        except self.model.DoesNotExist:
            return None










