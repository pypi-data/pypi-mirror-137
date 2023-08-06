from vtb_django_utils.user_info.info import set_user_info


class SetUserInfoMixin:
    """ Достает из реквеста инфо о пользователе и кладет в переменную контекста """
    # noinspection PyUnresolvedReferences
    def get_queryset(self, *args, **kwargs):
        set_user_info(self.request)
        return super(SetUserInfoMixin, self).get_queryset(*args, **kwargs)
