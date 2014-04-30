
from social_auth.middleware import SocialAuthExceptionMiddleware
from social_auth.exceptions import AuthCanceled


class RedirectOnCancelMiddleware(SocialAuthExceptionMiddleware):

    def get_redirect_uri(self, request, exception):
        if isinstance(exception, AuthCanceled):
            return '/signin'
        else:
            return super(RedirectOnCancelMiddleware, self).get_redirect_uri(request, exception)
