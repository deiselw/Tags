from django.http import HttpResponseBadRequest

def require_ajax(f):   
    def wrap(request, *args, **kwargs):
            if request.is_ajax():
                return f(request, *args, **kwargs)
            return HttpResponseBadRequest()
    wrap.__doc__=f.__doc__
    wrap.__name__=f.__name__
    return wrap