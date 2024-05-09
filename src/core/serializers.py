from rest_framework import serializers
from .models import Thread

class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = '__all__'


class ThreadCreateSerializer(serializers.Serializer):
    participant_id = serializers.IntegerField()
