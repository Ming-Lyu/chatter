from django import forms
from chatter.models import Dialog, Message

class DialogForm(forms.ModelForm):
    '''Basic dialog form 
    '''
    class Meta:
        model = Dialog
        exclude = ('owner', 'workflow_state')


class MessageForm(forms.ModelForm):
    '''Basic message form 
    '''
    class Meta:
        model = Message
        fields = ('content', )

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['content'].widget.attrs.setdefault('class', '')
