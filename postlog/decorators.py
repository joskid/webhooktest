from django.http import Http404
from django.conf import settings
from django.http import HttpResponse

def session_key_required(func):
    """ Implements own security check - user can see thread post only over GET request with thread_id in session. 
    I.e. with the same browser session."""

    def wrap(request, thread_id, *args, **kwargs):
        if request.method == 'GET' and not request.GET:
             if thread_id not in request.session.get('threads', []):
                raise Http404
        return func(request, thread_id, *args, **kwargs)
    return wrap

def set_headers(headers):
    """ Sets Access Control request headers (it's better to configure apache for that)."""
    def dec(func):
        def wrap(request, *args, **kwargs):
            # Firefox sends 'OPTIONS' request for cross-domain javascript call.
            if request.method != "OPTIONS": 
                response = func(request, *args, **kwargs)
            else:
                response = HttpResponse()
            for k, v in headers.iteritems():
                response[k] = v
            return response
        return wrap
    return dec
