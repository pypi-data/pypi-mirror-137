from django.apps import AppConfig


class OAuthBackendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'xdj_oauth'
    url_prefix = "oauth"
