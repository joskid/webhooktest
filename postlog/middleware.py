
class NginxMiddleware(object):
    """
    Fixes some Nginx-Apache specific issues. 
    """
    def process_request(self, request):
        request.is_secure = lambda: 'HTTP_X_FORWARDED_PROTOCOL' in request.META
        request.META['REMOTE_ADDR'] = request.META.get(
            'HTTP_X_FORWARDED_FOR', request.META.get(
                'HTTP_X_REAL_IP', request.META['REMOTE_ADDR']))

            
