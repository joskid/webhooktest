from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.http import HttpResponse
from django.conf import settings

from annoying.decorators import render_to
from postlog.models import Thread, Post
from postlog.forms import ThreadForm
from postlog.decorators import session_key_required, cross_domain_ajax
from postlog import signals

import uuid
from datetime import datetime


@render_to('homepage.html')
def homepage(request):
    """ The Home Page - creates a Webhook Thread. """
    threads = Thread.objects.from_request(request)
    form = ThreadForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        thread = form.save(request)
        Thread.objects.add_to_session(request, thread)
        return redirect(webhook_thread, thread.uuid)
    return locals()

@cross_domain_ajax
@session_key_required
@render_to('webhook_thread.html')
def webhook_thread(request, thread_id):
    """ Displays POSTs of a user's thread """
    thread = get_object_or_404(Thread, uuid=thread_id)
    threads = Thread.objects.from_request(request)
    form = ThreadForm(instance=thread)
    if request.POST or request.GET:
        post = Post.objects.create(thread=thread)
        signals.post_added.send(sender=Post.__class__,
                                request=request,
                                post=post)
        return HttpResponse('WebHook data has been successfully added.')
    posts_count = thread.posts.count()
    thread_url = request.build_absolute_uri(thread.get_absolute_url())
    return locals()

@session_key_required
def delete_post(request, thread_id, post_number):
    """ Deletes POST item from the given thread. """
    post = get_object_or_404(Post, number=post_number, thread__uuid=thread_id)
    thread = post.thread
    if request.method == 'GET':
        # delete object on GET only.
        post.delete()
    return redirect(webhook_thread, thread.uuid)


@session_key_required
def delete_thread(request, thread_id):
    """ Deletes the whole thread instance. """
    thread = get_object_or_404(Thread, uuid=thread_id)
    if request.method == 'GET':
        # delete object on GET only.
        thread.delete()
    return redirect(homepage)

@session_key_required
def update_thread(request, thread_id):
    """ Sets target_url for the given thread. """
    thread = get_object_or_404(Thread, uuid=thread_id)
    if request.method == 'POST':
        form = ThreadForm(request.POST, instance=thread)
        if form.is_valid():
            form.save(request)
    return redirect(webhook_thread, thread.uuid)

@cross_domain_ajax
def test_post(request):
    """ Just for testing. """
    response = HttpResponse('Your WebHook works fine! :)')
    print request.POST
    return response
