from chatter.models import Dialog
from rest_framework import serializers


class DialogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dialog
        fields = '__all__'
