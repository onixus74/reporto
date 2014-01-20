import logging
logger = logging.getLogger(__name__)

from django.utils.translation import ugettext as _

from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib import messages


staff_required = user_passes_test(lambda u: u.is_staff)
superuser_required = user_passes_test(lambda u: u.is_superuser)
reform_member_required = user_passes_test(lambda u: u.groups.filter(name='REFORM').count() == 0)


def login_required_with_message(view_func):
    decorated_view_func = login_required(view_func, login_url='home')

    def modified_view_func(request, *args, **kwargs):
        if not request.user.is_authenticated():
            messages.warning(request, 'Sorry, your need to sign in in order to proceed.')
        return decorated_view_func(request, *args, **kwargs)
    return modified_view_func

administrator_required = user_passes_test(lambda user: user.is_authenticated() and user.is_admin())
moderator_required = user_passes_test(lambda user: user.is_authenticated() and user.is_moderator())
reporter_required = user_passes_test(lambda user: user.is_authenticated() and user.is_reporter())
