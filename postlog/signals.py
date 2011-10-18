from django.dispatch import Signal

# Post object has been added to a Thread
post_added = Signal(providing_args=['request', 'post'])

