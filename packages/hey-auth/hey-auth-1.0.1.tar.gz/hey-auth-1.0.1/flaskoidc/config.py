import os


class OIDC_PROVIDERS:
    GOOGLE = "google"
    OKTA = "okta"
    KEYCLOAK = "keycloak"
    CUSTOM = "custom"


# All the custom configurations required for an OIDC provider to work with Authlib
# will go in here. We'll pass these while registering a client.
_CONFIGS = {
    OIDC_PROVIDERS.GOOGLE: {
        "authorize_params": {"access_type": "offline", "prompt": "consent"}
    },
    OIDC_PROVIDERS.OKTA: {},
    OIDC_PROVIDERS.KEYCLOAK: {},
    OIDC_PROVIDERS.CUSTOM: {},
}


class BaseConfig(object):
    SECRET_KEY = os.environ.get("FLASK_OIDC_SECRET_KEY", "!-flask-oidc-secret-key")
    WHITELISTED_ENDPOINTS = os.environ.get(
        "FLASK_OIDC_WHITELISTED_ENDPOINTS", "status,healthcheck,health"
    )

    OIDC_PROVIDER = os.environ.get("FLASK_OIDC_PROVIDER_NAME", "keycloak")
    OIDC_SCOPES = os.environ.get("FLASK_OIDC_SCOPES", "openid email profile")
    USER_ID_FIELD = os.environ.get("FLASK_OIDC_USER_ID_FIELD", "sub")
    CLIENT_ID = os.environ.get("FLASK_OIDC_CLIENT_ID", "")
    CLIENT_SECRET = os.environ.get("FLASK_OIDC_CLIENT_SECRET", "")
    SCHEME = os.environ.get("FLASK_OIDC_FORCE_SCHEME", "http")
    REDIRECT_URI = os.environ.get("FLASK_OIDC_REDIRECT_URI", "/auth")
    OVERWRITE_REDIRECT_URI = os.environ.get("FLASK_OIDC_OVERWRITE_REDIRECT_URI", "/")
    CONFIG_URL = os.environ.get("FLASK_OIDC_CONFIG_URL", "")
    # OAuth role: client or server (resource server) In our case, client means that
    # authentication in done through Flask, using /login and /auth endpoints. Server means
    # that the app is authenticated by either passing a refresh token to the /token endpoint
    # or by passing an access token in your request.
    ROLE = os.environ.get("FLASK_OIDC_ROLE", "client")
    # Access type options for Keycloak: public/confidential/bearer-only
    ACCESS_TYPE = os.environ.get("FLASK_OIDC_ACCESS_TYPE", "confidential")
    # Userinfo keys to return in user object
    USER_DETAILS_KEYS = os.environ.get("FLASK_OIDC_USER_DETAILS_KEYS", "preferred_username,email,name,given_name,family_name,email_verified")

    OIDC_PROVIDER_PARAMETERS_FILE = os.environ.get(
        "FLASK_OIDC_PROVIDER_ADDITIONAL_PARAMETERS_FILE_PATH", None
    )
    if OIDC_PROVIDER_PARAMETERS_FILE:
        import json

        with open(OIDC_PROVIDER_PARAMETERS_FILE) as parameters_file:
            parameters = json.load(parameters_file)
            _CONFIGS[OIDC_PROVIDER] = parameters

    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get(
        "SQLALCHEMY_TRACK_MODIFICATIONS", False
    )
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "SQLALCHEMY_DATABASE_URI", "sqlite:///sessions.db"
    )

    INVALID_TOKEN_MESSAGE = "The access token used is invalid."
    NO_TOKEN_MESSAGE = "Use of resource server requires that you pass an access token."
    EXPIRED_TOKEN_MESSAGE = "The access token has expired."
