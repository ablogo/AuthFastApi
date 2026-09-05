from log2mongo import log2mongo
import google_auth_oauthlib.flow
from dependency_injector.wiring import Provide, inject

from src.dependency_injection.containers import Container

log_service: log2mongo = Provide[Container.logging]

@inject
async def get_auth_url(log = log_service):
    try:
        oauth_client = Container.config.d()["GOOGLE_OAUTH_CLIENT"]
        oauth_id = Container.config.d()["GOOGLE_OAUTH_ID"]
        oauth_js_origins = Container.config.d()["GOOGLE_OAUTH_JS_ORIGINS"]
        oauth_secret = Container.config.d()["GOOGLE_OAUTH_SECRET"]
        oauth_scopes = Container.config.d()["GOOGLE_OAUTH_SCOPES"]
        oauth_redirect_response = Container.config.d()["GOOGLE_OAUTH_REDIRECT_RESPONSE"]
        
        flow = google_auth_oauthlib.flow.Flow.from_client_config(
            {"web":{"client_id":oauth_client,"project_id":oauth_id,"auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":oauth_secret,"javascript_origins":oauth_js_origins.split(',') if oauth_js_origins else []}},
            scopes = oauth_scopes.split(',') if oauth_scopes else []
        )
        flow.redirect_uri = oauth_redirect_response

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
        oauth_client = Container.config.d()["GOOGLE_OAUTH_CLIENT"]
        oauth_id = Container.config.d()["GOOGLE_OAUTH_ID"]
        oauth_js_origins = Container.config.d()["GOOGLE_OAUTH_JS_ORIGINS"]
        oauth_secret = Container.config.d()["GOOGLE_OAUTH_SECRET"]
        oauth_scopes = Container.config.d()["GOOGLE_OAUTH_SCOPES"]
        oauth_redirect_response = Container.config.d()["GOOGLE_OAUTH_REDIRECT_RESPONSE"]

        flow = google_auth_oauthlib.flow.Flow.from_client_config(
            {"web":{"client_id":oauth_client,"project_id":oauth_id,"auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":oauth_secret,"javascript_origins":oauth_js_origins.split(',') if oauth_js_origins else []}},
            scopes = oauth_scopes.split(',') if oauth_scopes else []
        )
        flow.redirect_uri = oauth_redirect_response

        auth_reponse = flow.fetch_token(authorization_response = url)
        credentials = flow.credentials

    except Exception as e:
        log.logger.error(e)
    finally:
        return credentials