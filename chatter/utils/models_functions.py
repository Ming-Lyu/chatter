from django.db.models import Aggregate, CharField


import django
if django.VERSION >= (3, 1, 0):
    from django.db.models import JSONField
else:
    from django.contrib.postgres.fields import JSONField


class Concat(Aggregate):
    function = 'GROUP_CONCAT'
    template = '%(function)s(%(distinct)s%(expressions)s)'

    def __init__(self, expression, distinct=False, **extra):
        super(Concat, self).__init__(
            expression,
            distinct='DISTINCT ' if distinct else '',
            output_field=JSONField(),
            **extra)