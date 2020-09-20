from chatter.models import Dialog
from .serializers import DialogSerializer
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action

class DialogViewSet(viewsets.ModelViewSet):
    queryset = Dialog.objects.all()
    serializer_class = DialogSerializer

    def get_queryset(self):
        # TODO with opponent: not necessarily in one model
        return Dialog.objects.filter(owner=self.request.user).order_by('-created')

    # @action
    # def send(self, request, pk=None):
    #     pass

    # @action
    # def withdrawl(self, request, pk=None):
    #     pass