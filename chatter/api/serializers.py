from chatter.models import Dialog, Message
from django.contrib.auth.models import User
from rest_framework import serializers

class MessageSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='owner')
    message = serializers.CharField(source='content')
    class Meta:
        model = Message
        fields = ('message', 'author', 'id')
class DialogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dialog
        fields = '__all__'


