import inspect


def single_org(method):
    signature = inspect.signature(method)

    def wrapper(self, *args, **kwargs):

        bound = signature.bind(*((self,) + args), **kwargs)

        bound.apply_defaults()

        k = "org_id"

        if k in bound.arguments:
            v = bound.arguments[k]
            bound.arguments.update({k: v if v else getattr(self, k)})

        return method(*bound.args, **bound.kwargs)

    return wrapper
