from django.http import Http404
from django.conf import settings
from django.http import HttpResponse

ACC_HEADERS = {'Access-Control-Allow-Origin': '*', 
               'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
               'Access-Control-Max-Age': 1000,
               'Access-Control-Allow-Headers': '*'}

def session_key_required(func):
    """ Implements own security check - user can see thread post only over GET request with thread_id in session. 
    I.e. with the same browser session."""

    def wrap(request, thread_id, *args, **kwargs):
        if request.method == 'GET' and not request.GET:
             if thread_id not in request.session.get('threads', []):
                raise Http404
        return func(request, thread_id, *args, **kwargs)
    return wrap


def cross_domain_ajax(func):
    """ Sets Access Control request headers."""
    def wrap(request, *args, **kwargs):
        # Firefox sends 'OPTIONS' request for cross-domain javascript call.
        if request.method != "OPTIONS": 
            response = func(request, *args, **kwargs)
        else:
            response = HttpResponse()
        for k, v in ACC_HEADERS.iteritems():
            response[k] = v
        return response
    return wrap
