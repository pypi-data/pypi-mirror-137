import logging
from authlib.integrations.flask_client import OAuth
from authlib.oidc.core.errors import LoginRequiredError
from flask import Flask, request, session, jsonify, abort, redirect
from flask.helpers import get_env, get_debug_flag, make_response, url_for
from flask_sqlalchemy import SQLAlchemy
from flaskoidc.config import BaseConfig, _CONFIGS

LOGGER = logging.getLogger(__name__)


class FlaskOIDC(Flask):
    def _before_request(self):
        # Whitelisted Endpoints i.e., health checks and status url
        whitelisted_endpoints = self.config.get("WHITELISTED_ENDPOINTS")
        LOGGER.debug(f"Whitelisted Endpoint: {whitelisted_endpoints}")

        # Add auth endpoints to whitelisted endpoint as well, so not to check for token on that
        whitelisted_endpoints += (
            f",login,logout,token,{self.config.get('REDIRECT_URI').strip('/')}"
        )

        if request.path.strip("/") in whitelisted_endpoints.split(",") or \
                request.endpoint in whitelisted_endpoints.split(","):
            return

        try:
            assert self.auth_client.token
        except LoginRequiredError as e:
            if self.config.get("ROLE") == "client":
                LOGGER.exception(
                    "User not logged in, redirecting to auth", exc_info=True
                )
                return redirect(url_for("logout", _external=True))
            else:
                abort(make_response(jsonify({"message": e.description}), 401))

    def __init__(self, *args, **kwargs):
        super(FlaskOIDC, self).__init__(*args, **kwargs)

        self.db = SQLAlchemy(self)
        _provider = self.config.get("OIDC_PROVIDER").lower()

        if _provider not in _CONFIGS.keys():
            LOGGER.info(
                f"""
            [flaskoidc Notice] I have not verified the OIDC Provider that you have 
            selected i.e., "{_provider}" with this package yet. 
            If you encounter any issue while using this library with "{_provider}",
            please do not hesitate to create an issue on Github. (https://github.com/verdan/flaskoidc)
            """
            )

        with self.app_context():
            from flaskoidc.auth_client import FlaskAuthClient

            self.db.create_all()

            oauth = OAuth(self)

            self.auth_client = oauth.register(
                name=_provider,
                client_cls=FlaskAuthClient,
                server_metadata_url=self.config.get("CONFIG_URL"),
                client_kwargs={
                    "scope": self.config.get("OIDC_SCOPES"),
                },
                **_CONFIGS.get(_provider) if _CONFIGS.get(_provider) else {},
            )

        # Register the before request function that will make sure each
        # request is authenticated before processing
        self.before_request(self._before_request)

        @self.route("/login")
        def login():
            redirect_uri = url_for("auth", _external=True, _scheme=self.config.get("SCHEME"))
            return self.auth_client.authorize_redirect(redirect_uri)

        @self.route(self.config.get("REDIRECT_URI"))
        def auth():
            try:
                token = self.auth_client.authorize_access_token()
                self.auth_client.handle_auth_token(token)
                return redirect(self.config.get("OVERWRITE_REDIRECT_URI"))
            except Exception as ex:
                LOGGER.exception(ex)
                raise ex

        @self.route("/token", methods=["POST"])
        def token():
            data = request.form.to_dict()
            token = self.auth_client.refresh_token(data["refresh_token"])
            # fixes 'missing nonce' which shouldn't happen in production:
            # session.pop("_keycloak_authlib_nonce_")
            user = self.auth_client.handle_auth_token(token)
            user_details_keys = self.config.get('USER_DETAILS_KEYS', '').split(',')
            user_details = {key: val for key, val in user.items()
                            if key in user_details_keys}
            return make_response(jsonify(user_details), 200)

        @self.route("/logout")
        def logout():
            # ToDo: Think of if we should delete the session entity or not
            # if session.get("user"):
            #     OAuth2Token.delete(name=_provider, user_id=session["user"]["__id"])
            session.pop("user", None)
            if self.config.get("ROLE") == "client":
                return redirect(url_for("login"))    
            return make_response(jsonify({"message": "Logged out."}), 200)

    def make_config(self, instance_relative=False):
        """
        Overriding the default `make_config` function in order to support
        Flask OIDC package and all of their settings.
        """
        root_path = self.root_path
        if instance_relative:
            root_path = self.instance_path
        defaults = dict(self.default_config)
        defaults["ENV"] = get_env()
        defaults["DEBUG"] = get_debug_flag()

        _required_fields = ["CLIENT_ID", "CLIENT_SECRET", "CONFIG_URL"]

        # Append all the configurations from the base config class.
        for key, value in BaseConfig.__dict__.items():
            if not key.startswith("__"):
                if key in ["CLIENT_ID", "CLIENT_SECRET"]:
                    key = f"{BaseConfig.OIDC_PROVIDER.upper()}_{key}"

                if key in _required_fields and not value:
                    raise RuntimeError(
                        f"Invalid Configuration: {key} is required and can not be empty."
                    )

                defaults[key] = value
        return self.config_class(root_path, defaults)
