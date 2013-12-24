from django.contrib.auth.decorators import login_required, user_passes_test, \
  permission_required


staff_required = user_passes_test(lambda u: u.is_staff)
superuser_required = user_passes_test(lambda u: u.is_superuser)
reform_member_required = user_passes_test(lambda u: u.groups.filter(name='REFORM').count() == 0)

administrator_required = user_passes_test(lambda user: user.is_admin())
moderator_required = user_passes_test(lambda user: user.is_admin())
reporter_required = user_passes_test(lambda user: user.is_admin())
