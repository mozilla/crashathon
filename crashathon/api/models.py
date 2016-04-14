from django.db import models

from django.db.models import Count


def collect_id_counts(start, end, country=None, version=None):
    q = Crash.objects.filter(
        creation_date__gte=start,
        creation_date__lt=end)
    if country:
        q = q.filter(geo_country=country)
    if version:
        q = q.filter(app_version=version)
    return (q.values('client_id')
             .annotate(count=Count('client_id'))
             .order_by('-count')
             .values_list('count', flat=True))


class Crash(models.Model):
    class Meta:
        db_table = 'crash'
    client_id = models.UUIDField()
    app_version = models.CharField(max_length=8)
    creation_date = models.DateTimeField()
    geo_country = models.CharField(max_length=2)
