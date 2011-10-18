from django.db import models, IntegrityError
from django.conf import settings

from annoying.fields import JSONField
from django_extensions.db.models import TimeStampedModel

from postlog.managers import ThreadManager, PostManager
from postlog import signals
from postlog import utils

import uuid

class Thread(TimeStampedModel):
    """ User session-related container of POST data. """

    uuid = models.CharField(max_length=8, editable=False, unique=True, db_index=True,
                            help_text="URL-friendly thread UD.")
    client_ip = models.IPAddressField(null=True, blank=True, editable=False,
                                      help_text="IP of a user who created thread.")
    alias = models.CharField("Thread Alias", max_length=60, null=True, blank=True, 
                             help_text="Human-friendly name of your thread, for instance, 'Chargify WebHook'.")
    target_url = models.URLField("Target URL", null=True, blank=True, verify_exists=False, default="http://127.0.0.1:8000/",
                                 help_text="Your development server URL, i.e. 'http://127.0.0.1:8000/paypal-ipn/'.")
    
    objects = ThreadManager()

    def __unicode__(self):
        return self.alias or self.uuid

    def save(self, *args, **kwargs):
        if not self.uuid:
            # pretty straightforward URL generator.
            self.uuid = uuid.uuid4().hex[:6]
        try:
            super(Thread, self).save(*args, **kwargs)
        except IntegrityError:
            self.uuid = None
            self.save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('webhook-thread', [self.uuid])

    class Meta:
        ordering = ('-created',)


class Post(TimeStampedModel):
    """
    Stores request POST data and meta-info.
    """

    thread = models.ForeignKey(Thread, related_name='posts')
    remote_ip = models.IPAddressField(null=True, blank=True, 
                                      help_text="IP of webhook caller server.")
    number = models.IntegerField(help_text="Sequential number of Post at the thread.")
    data = JSONField(null=True, help_text="Request data dump.")

    objects = PostManager()

    def __unicode__(self):
        return u"%s" % self.number

    def get_remote_server(self):
        """ Tries to return server name first. If undefined returns IP address. """
        return self.data.get('Remote-Host', None) or self.remote_ip
    
    class Meta:
        ordering = ('-number',)

def handle_post(sender, request, post, **kwargs):
    """ Saves request dump. """
    post.data = dict(parsed_post=request.POST,
                     request_method=request.method,
                     parsed_get=request.GET,
                     raw_post=request.raw_post_data,
                     http_headers=utils.filter_request_headers(request))
    post.remote_ip=request.META.get('REMOTE_ADDR', None)
    post.save()

signals.post_added.connect(handle_post)
