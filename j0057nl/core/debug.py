def debug(request, message):
    if not message.endswith('\n'):
        message += '\n'
    request.environ['wsgi.errors'].write(message)

