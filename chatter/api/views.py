from chatter.models import Dialog, Message
from .serializers import DialogSerializer, MessageSerializer
from rest_framework import viewsets, generics
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination




class DialogViewSet(viewsets.ModelViewSet):
    queryset = Dialog.objects.all()
    serializer_class = DialogSerializer

    def get_queryset(self):
        # TODO with opponent: not necessarily in one model
        return Dialog.objects.filter(participants=self.request.user).order_by('-created')

    # @action
    # def send(self, request, pk=None):
    #     pass

    # @action
    # def withdrawl(self, request, pk=None):
    #     pass


class MessagePagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 1000
    
class MessageListViewSet(generics.ListAPIView):
    serializer_class = MessageSerializer
    pagination_class = MessagePagination

    def get_queryset(self):
        """
            This view should return a list of messages
            for the dialogs indicated.
        """
        dialog_id = self.request.GET.get('dialog_id', None)
        filter_obj = {}
        if dialog_id:
            filter_obj.update({'dialog_id':dialog_id})
        return Message.objects.filter(**filter_obj).order_by('-created')

