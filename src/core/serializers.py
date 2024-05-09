from rest_framework import serializers
from .models import Thread, Message
from django.contrib.auth.models import User


class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = '__all__'


class ThreadCreateSerializer(serializers.Serializer):
    participant_id = serializers.IntegerField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class MessageCreateSerializer(serializers.Serializer):
    text = serializers.CharField()


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    
    class Meta:
        model = Message
        fields = '__all__'
