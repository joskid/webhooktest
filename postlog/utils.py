
def filter_request_headers(request):
    """
    Returns http headers in standard-like format:
    ContentType: application/x-www-form-urlencoded
    """

    return dict(('-'.join(map(
                    lambda x: x.title(), key.split('_'))), val) for key, val in 
                request.META.items() if key.startswith('HTTP_') or 
                key.startswith('CONTENT_') or key.startswith('REMOTE_'))

    

