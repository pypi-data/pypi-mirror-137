from vtb_django_utils.user_info.info import set_user_info


class SetUserInfoMixin:
    """ Достает из реквеста инфо о пользователе и кладет в переменную контекста """
    # noinspection PyUnresolvedReferences
    def initialize_request(self, request, *args, **kwargs):
        request = super().initialize_request(request, *args, **kwargs)
        set_user_info(request)
        return request
