from rest_framework import serializers

class CheckboxActionSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    action = serializers.ChoiceField(choices=['check', 'uncheck'])
