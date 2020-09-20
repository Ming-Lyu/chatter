from django import forms
from chatter.forms import Dialog

class DialogForm(forms.ModelForm):
    '''Basic dialog form 
    '''
    class Meta:
        model = Dialog
        exclude = ('owner', 'workflow_state')
