class PromEndpoints:

    _prom_host = 'prom.ua'

    @staticmethod
    def favorites():
        return f'https://my.{PromEndpoints._prom_host}/cabinet/user/favorites'

    @staticmethod
    def velosipednye_shiny():
        return f'https://{PromEndpoints._prom_host}/Velosipednye-shiny'


gorest_users_url = 'https://gorest.co.in/public/v2/users'
