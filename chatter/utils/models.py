### COPYRIGHT: modelutils

from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext as _


class AutoCreatedField(models.DateTimeField):
    """
    A DateTimeField that automatically populates itself at
    object creation.
    By default, sets editable=False, default=datetime.now.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('editable', False)
        kwargs.setdefault('default', now)
        super().__init__(*args, **kwargs)


class AutoLastModifiedField(AutoCreatedField):
    """
    A DateTimeField that updates itself on each save() of the model.
    By default, sets editable=False and default=datetime.now.
    """
    def get_default(self):
        """Return the default value for this field."""
        if not hasattr(self, "_default"):
            self._default = self._get_default()
        return self._default

    def pre_save(self, model_instance, add):
        value = now()
        if add:
            current_value = getattr(model_instance, self.attname, self.get_default())
            if current_value != self.get_default():
                # when creating an instance and the modified date is set
                # don't change the value, assume the developer wants that
                # control.
                value = getattr(model_instance, self.attname)
            else:
                for field in model_instance._meta.get_fields():
                    if isinstance(field, AutoCreatedField):
                        value = getattr(model_instance, field.name)
                        break
        setattr(model_instance, self.attname, value)
        return value


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created`` and ``modified`` fields.
    """
    created = AutoCreatedField(_('created'))
    modified = AutoLastModifiedField(_('modified'))

    def save(self, *args, **kwargs):
        """
        Overriding the save method in order to make sure that
        modified field is updated even if it is not given as
        a parameter to the update field argument.
        """
        if 'update_fields' in kwargs and 'modified' not in kwargs['update_fields']:
            kwargs['update_fields'] += ['modified']
        super().save(*args, **kwargs)

    class Meta:
        abstract = True