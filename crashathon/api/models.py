from django.db import models

from django.db.models import Count


def collect_id_counts(start, end):
    return Crash.objects.filter(
        creation_date__gte=start,
        creation_date__lt=end
    ).values('client_id').annotate(count=Count('client_id')).order_by("-count")


class Crash(models.Model):
    class Meta:
        db_table = 'crash'
    client_id = models.UUIDField()
    app_version = models.CharField(max_length=8)
    creation_date = models.DateField()
    geo_country = models.CharField(max_length=2)
