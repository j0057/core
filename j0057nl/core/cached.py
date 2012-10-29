import j0057nl.core
import j0057nl.core.basedec 

def cached(size):
    def closure(SIZE, CACHE, KEYS):
        class cached(j0057nl.core.basedec.BaseDecorator):
            def __init__(self, func):
                self.func = func
            def __call__(self, request, *a, **k):
                key = a
                j0057nl.core.debug(request, 'Cache({0}): Cache object is 0x{1:x}'.format(SIZE, id(CACHE)))
                j0057nl.core.debug(request, 'Cache({0}): Checking for key {1}'.format(SIZE, key))
                if key in CACHE:
                    j0057nl.core.debug(request, 'Cache({0}): Hit key {1}'.format(SIZE, key))
                else:
                    j0057nl.core.debug(request, 'Cache({0}): Miss key {1}'.format(SIZE, key))
                    CACHE[key] = self.func(request, *a, **k)
                    KEYS.append(key)
                    if len(KEYS) > SIZE:
                        oldest = KEYS.pop(0)
                        j0057nl.core.debug(request, 'Cache({0}): Purging key {1}'.format(SIZE, oldest))
                        del CACHE[oldest]
                CACHE[key].body_stream.seek(0)
                return CACHE[key]
        return cached
    cache, keys = {}, []
    return closure(size, cache, keys)

