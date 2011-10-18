from django import forms

from postlog.models import Thread

class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ('alias', 'target_url')

    def save(self, request, commit=True):
        self.instance.client_ip = request.META.get('REMOTE_ADDR', None)
        return super(ThreadForm, self).save(commit=commit)

