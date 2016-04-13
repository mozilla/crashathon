import datetime
import itertools
import uuid

from django.test import TestCase

from rest_framework.reverse import reverse

from crashathon.api.models import Crash


class TestCrashHistogramView(TestCase):
    def setUp(self):
        self.url = reverse('crash_histogram')

    def test_basic(self):
        """
        Requests for a date range return a list of client ids and crash counts.
        """
        dayctr = (datetime.date(2016, 1, 1) + datetime.timedelta(days=i)
                  for i in itertools.count())
        counts = [10, 6, 2, 1]
        uuids = [uuid.uuid4() for _ in counts]
        for i, client_id in zip(counts, uuids):
            for _ in range(i):
                Crash.objects.create(
                    client_id=client_id,
                    app_version='45.0',
                    geo_country='US',
                    creation_date=next(dayctr))
        res = self.client.get(self.url, data={"start": "20160101",
                                              "end": "20160201"})
        self.assertEqual(res.json(), {"crashes": counts})

    def test_country_filter(self):
        """
        Records are excluded from crash counts that do not match country.
        """
        client_id = uuid.uuid4()
        Crash.objects.create(
            client_id=client_id,
            app_version='45.0',
            geo_country='DE',
            creation_date=datetime.date(2016, 1, 15))
        Crash.objects.create(
            client_id=client_id,
            app_version='45.0',
            geo_country='DE',
            creation_date=datetime.date(2016, 1, 16))
        Crash.objects.create(
            client_id=client_id,
            app_version='45.0',
            geo_country='PL',
            creation_date=datetime.date(2016, 1, 15))
        res = self.client.get(self.url, data={"start": "20160101",
                                              "end": "20160201",
                                              "country": "DE"})
        self.assertEqual(res.json(), {"crashes": [2]})

        res = self.client.get(self.url, data={"start": "20160101",
                                              "end": "20160201",
                                              "country": "PL"})
        self.assertEqual(res.json(), {"crashes": [1]})

    def test_version_filter(self):
        """
        Records are excluded that do not match version.
        """
        client_id = uuid.uuid4()
        Crash.objects.create(
            client_id=client_id,
            app_version='44.0',
            geo_country='DE',
            creation_date=datetime.date(2016, 1, 15))
        Crash.objects.create(
            client_id=client_id,
            app_version='45.0',
            geo_country='US',
            creation_date=datetime.date(2016, 1, 16))
        Crash.objects.create(
            client_id=client_id,
            app_version='45.0',
            geo_country='PL',
            creation_date=datetime.date(2016, 1, 15))
        res = self.client.get(self.url, data={"start": "20160101",
                                              "end": "20160201",
                                              "version": "45.0"})
        self.assertEqual(res.json(), {"crashes": [2]})

        res = self.client.get(self.url, data={"start": "20160101",
                                              "end": "20160201",
                                              "version": "44.0"})
        self.assertEqual(res.json(), {"crashes": [1]})

    def test_invalid_date(self):
        """
        Invalid dates are rejected.
        """
        res = self.client.get(self.url, data={"start": "Juvember 7th",
                                              "end": "20160201"})
        self.assertEqual(res.status_code, 400)

    def test_missing_date(self):
        """
        Histogram requests must have date bounds.
        """
        res = self.client.get(self.url, data={"end": "20160201"})
        self.assertEqual(res.status_code, 400)
        res = self.client.get(self.url, data={"start": "20160101"})
        self.assertEqual(res.status_code, 400)
