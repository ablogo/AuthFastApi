import google.oauth2.credentials
from log2mongo import log2mongo
import google_auth_oauthlib.flow
from dependency_injector.wiring import Provide, inject

from src.dependency_injection.containers import Container

log_service: log2mongo = Provide[Container.logging]
config = Container.config.d()

@inject
async def get_auth_url(log = log_service):
    try:
        flow = google_auth_oauthlib.flow.Flow.from_client_config(
            {"web":{"client_id":config["GOOGLE_OAUTH_CLIENT"],"project_id":config["GOOGLE_OAUTH_ID"],"auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":config["GOOGLE_OAUTH_SECRET"],"javascript_origins":config["GOOGLE_OAUTH_JS_ORIGINS"].split(',') if config["GOOGLE_OAUTH_JS_ORIGINS"] else []}},
            scopes = config["GOOGLE_OAUTH_SCOPES"].split(',') if config["GOOGLE_OAUTH_SCOPES"] else []
        )
        flow.redirect_uri = config["GOOGLE_OAUTH_REDIRECT_RESPONSE"]

        auth_url , state = flow.authorization_url(
            acces_type = 'offline',
            include_grand_scopes = 'true',
            prompt = 'consent'
        )

        return auth_url

    except Exception as e:
        log.logger.error(e)

@inject
async def get_auth_response(url: str, log = log_service):
    try:
        credentials = None
        flow = google_auth_oauthlib.flow.Flow.from_client_config(
            {"web":{"client_id":config["GOOGLE_OAUTH_CLIENT"],"project_id":config["GOOGLE_OAUTH_ID"],"auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":config["GOOGLE_OAUTH_SECRET"],"javascript_origins":config["GOOGLE_OAUTH_JS_ORIGINS"].split(',') if config["GOOGLE_OAUTH_JS_ORIGINS"] else []}},
            scopes = config["GOOGLE_OAUTH_SCOPES"].split(',') if config["GOOGLE_OAUTH_SCOPES"] else []
        )
        flow.redirect_uri = config["GOOGLE_OAUTH_REDIRECT_RESPONSE"]

        auth_reponse = flow.fetch_token(authorization_response = url)
        credentials = flow.credentials

    except Exception as e:
        log.logger.error(e)
    finally:
        return credentials