from rest_framework import serializers

class BulkActivationSerializer(serializers.Serializer):
    user_ids = serializers.ListField(child=serializers.IntegerField(), allow_empty=False)
    is_active = serializers.BooleanField()
