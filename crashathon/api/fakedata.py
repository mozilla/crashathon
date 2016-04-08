import datetime
import random
import uuid

from django.db import transaction

from crashathon.api.models import Crash

BUCKETS = [8747, 1486, 662, 639, 247, 79, 43, 40, 32, 4]
appversions = ['45.0a2', '45.0b1', '45.0', '44.0']
dates = [datetime.date(2016, 1, 1) + datetime.timedelta(days=i)
         for i in range(180)]
countries = ['US', 'PT', 'ES', 'DE', 'CO', 'PL', 'JP', 'BR', 'VE']


def generate_fake_data(buckets=BUCKETS):
    for i, size in enumerate(buckets):
        left, right = i * 10, (i + 1) * 10
        with transaction.atomic():
            for _ in range(size):
                client_id = uuid.uuid4()
                for _ in range(random.randrange(left, right)):
                    Crash.objects.create(
                        client_id=client_id,
                        app_version=random.choice(appversions),
                        creation_date=random.choice(dates),
                        geo_country=random.choice(countries))
