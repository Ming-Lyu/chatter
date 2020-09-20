from chatter.models import Dialog
from .serializers import DialogSerializer
from rest_framework import viewsets
class DialogViewSet(viewsets.ModelViewSet):
    queryset = Dialog.objects.all()
    serializer_class = DialogSerializer
