import functools

from flask import request
from werkzeug.exceptions import NotAcceptable
from functools import partial


class Acceptor(object):
    mimetypes = []
    use_fallback = False

    def __init__(self, func):
        """Initialize a new Acceptor and create the accept handlers

        :param func: the endpoint function to fall back upon
        """
        self.fallback = func
        self.accept_handlers = {
            mimetype: func for mimetype in self.mimetypes
        }
        functools.update_wrapper(self, func)

    def __call__(self, *args, **kwargs):
        """Select a handler function to respond to the preferred mediatypes."""

        for mimetype in request.accept_mimetypes.values():
            if mimetype in self.accept_handlers:
                return self.accept_handlers[mimetype](*args, **kwargs)

        if self.use_fallback:
            return self.fallback(*args, **kwargs)

        supported_types = ', '.join(self.accept_handlers)
        description = '{} Supported entities are: {}'.format(
            NotAcceptable.description, supported_types)
        raise NotAcceptable(description)

    def __get__(self, instance, owner):
        return partial(self.__call__, instance)

    def support(self, *mimetypes):
        """Register an additional mediatype handler on an existing Acceptor."""

        def decorator(func):
            for mimetype in mimetypes:
                self.accept_handlers[mimetype] = func
            return func
        return decorator


def accept(*args):
    """Decorator to explictly allows multiple mediatypes

    :param args: the accepted mediatypes, as strings
    :returns: an Acceptor class to be initialized
    """

    class ExplicitAcceptor(Acceptor):
        mimetypes = args

    return ExplicitAcceptor


def accept_fallback(func):
    """Decorator to specify a fallback endpoint function.

    :param func: the endpoint function to fall back upon
    :returns: an initialized Acceptor
    """

    class FallbackAcceptor(Acceptor):
        use_fallback = True

    return FallbackAcceptor(func)
