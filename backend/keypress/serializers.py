from rest_framework import serializers

class CheckboxActionSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    action = serializers.ChoiceField(choices=['check', 'uncheck'])

class ApplicationListSerializer(serializers.Serializer):
    windows = serializers.ListField(child=serializers.CharField(max_length=255))

class WindowSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    class_name = serializers.CharField(max_length=255)
    handle = serializers.IntegerField()