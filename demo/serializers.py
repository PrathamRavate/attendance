from rest_framework import serializers


class GetProfileRequestSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()


class GetProfileResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    employee_id = serializers.IntegerField()
    name = serializers.CharField()
    email = serializers.EmailField()
    entry_log_time = serializers.DateTimeField()
    exit_log_time = serializers.DateTimeField()
    time_difference = serializers.TimeField()
