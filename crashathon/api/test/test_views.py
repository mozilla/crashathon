from django.test import TestCase

from rest_framework.reverse import reverse

from crashathon.api.views import FAKE_DATA


class TestCrashHistogramView(TestCase):
    def setUp(self):
        self.url = reverse('crash_histogram')

    def test_basic(self):
        """
        Requests for a date range return a list of crash-stats buckets.
        """
        res = self.client.get(self.url, data={"start": "20160101",
                                              "end": "20160201"})
        self.assertEqual(res.json(), {
            "binSize": 10, "numBins": 10,
            "bins": FAKE_DATA})

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

    def _fixture_teardown(self):
        pass
