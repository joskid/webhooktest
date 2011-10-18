from django.db import models

class ThreadManager(models.Manager):

    def from_request(self, request):
        return self.get_query_set().filter(uuid__in=request.session.get('threads', []))

    def add_to_session(self, request, thread):
        threads = request.session.get('threads', [])
        threads.append(thread.uuid)
        request.session['threads'] = threads
        request.session.modified = True

class PostManager(models.Manager):
    
    def create(self, **kwargs):
        kwargs['number'] = self.get_query_set().filter(
            thread=kwargs['thread']).count() + 1
        return self.get_query_set().create(**kwargs)
