from django.conf.urls.defaults import *

urlpatterns = patterns('postlog.views',
    url(r'^$', 'homepage',  name='homepage'),
    url(r'^test/', 'test_post',  name='test-post'),
    url(r'^(?P<thread_id>[a-zA-Z0-9_.-]+)/$', 'webhook_thread',  name='webhook-thread'),
    url(r'^(?P<thread_id>[a-zA-Z0-9_.-]+)/delete/$', 'delete_thread',  name='delete-thread'),
    url(r'^(?P<thread_id>[a-zA-Z0-9_.-]+)/update/$', 'update_thread',  name='update-thread'),
    url(r'^(?P<thread_id>[a-zA-Z0-9_.-]+)/delete/(?P<post_number>\d+)/$', 'delete_post',  name='delete-post'),
    url(r'^test/', 'test_post',  name='test-post'),
)
