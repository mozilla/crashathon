# from django.conf import settings

# import elasticsearch
# from elasticsearch_dsl import Search
from rest_framework.exceptions import ParseError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


from crashathon.api.forms import StatsForm

FAKE_DATA = [27341, 31492, 12048, 3019, 462, 179, 184, 2, 21, 563]


class CrashView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def perform_authentication(self, request):
        pass

    def get(self, request):
        form = StatsForm(request.GET)
        if not form.is_valid():
            exc = ParseError()
            exc.detail = {'detail': dict(form.errors.items())}
            raise exc
        # es = elasticsearch.Elasticsearch(hosts=settings.ES_HOSTS)
        # qs = Search(using=es, index='crashes', doc_type='crash').filter(
        #     "range", date={"gte": form.start, "lt": form.end})
        return Response({"binSize": 10, "numBins": 10,
                         "bins": FAKE_DATA})
