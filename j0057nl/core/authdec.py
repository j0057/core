import webob
import webob.exc

import j0057nl.core.basedec

def authenticated(*rights):
    class authenticated(j0057nl.core.basedec.BaseDecorator):
        def __init__(self, func):
            self.func = func
        def __call__(self, request, *args):
            if request.session is None:
                raise webob.exc.HTTPForbidden('No session found; log in first.')
            missing = [ right for right in rights 
                        if right not in request.session.rights ]
            if missing:
                raise webob.exc.HTTPForbidden('Missing rights: ' + repr(missing))
            return self.func(request, *args)
    return authenticated
