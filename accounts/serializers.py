from rest_framework import serializers

class RelatorioPDFSerializer(serializers.Serializer):
    animal_id = serializers.IntegerField(required=True)