from django.db import models

class ThreadManager(models.Manager):

    def from_request(self, request):
        """ Returns query set of Thread objects linked with the request. """
        return self.get_query_set().filter(uuid__in=request.session.get('threads', []))

    def add_to_session(self, request, thread):
        """ Links Thread with the request. """
        threads = request.session.get('threads', [])
        threads.append(thread.uuid)
        request.session['threads'] = threads
        request.session.modified = True

class PostManager(models.Manager):
    
    def create(self, **kwargs):
        """ Replaces native 'create' to initialize ordering number. """
        try:
            kwargs['number'] = self.get_query_set().filter(
                thread=kwargs.get('thread', 0))[0].number + 1
        except IndexError:
            kwargs['number'] = 1
        return self.get_query_set().create(**kwargs)
