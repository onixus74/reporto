import logging
logger = logging.getLogger(__name__)


def get_user(strategy, user=None, *args, **kwargs):
	logger.debug('--------------------------------------------------------------------')
	logger.debug('USER %s', [strategy, user, args, kwargs])
	logger.debug('--------------------------------------------------------------------')
	if user:
		username = user.email
	else:
		username = strategy.session_get('saved_email')
	return {'username': username}


# def associate_by_email(details, user=None, *args, **kwargs):
#     """Return user entry with same email address as one returned on details."""
#     if user:
#         return None

#     email = details.get('email')

#     if email:
#         # Try to associate accounts registered with the same email address,
#         # only if it's a single object. AuthException is raised if multiple
#         # objects are returned.
#         try:
#             return {'user': UserSocialAuth.get_user_by_email(email=email)}
#         except MultipleObjectsReturned:
#             raise AuthException(kwargs['backend'], 'Not unique email address.')
#         except ObjectDoesNotExist:
#             pass
