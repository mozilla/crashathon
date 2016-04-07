from rest_framework import serializers


class CrashHistogramSerializer(serializers.Serializer):
    crashes = serializers.ListField(
        child=serializers.IntegerField(min_value=0))
