from rest_framework.exceptions import ParseError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


from crashathon.api.forms import StatsForm
from crashathon.api.models import collect_id_counts

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
        ids_and_counts = collect_id_counts(form.cleaned_data['start'],
                                           form.cleaned_data['end'])
        return Response({"crashes": list(ids_and_counts)})
