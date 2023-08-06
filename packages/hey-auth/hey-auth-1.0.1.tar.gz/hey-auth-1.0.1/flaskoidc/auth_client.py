import logging
from flask import session, request, _app_ctx_stack
from werkzeug.exceptions import BadRequest
from authlib.integrations.flask_client import FlaskRemoteApp
from authlib.oidc.core.errors import LoginRequiredError
from flaskoidc.models import OAuth2Token

LOGGER = logging.getLogger(__name__)


class FlaskAuthClient(FlaskRemoteApp):
    """Extension of FlaskRemoteApp, the default client class used by Flask OAuth.
    self.auth_client seen in __init__.py is an instance of this class. This class
    implements additional checking for token expiration and automatic token refresh.
    """

    @property
    def token(self):
        """Extended implementation of the FlaskRemoteApp token property. First checks
        if a token has already been set. If not, collects a token from the database and
        refreshes if expired.
        """
        ctx = _app_ctx_stack.top
        attr = 'authlib_oauth_token_{}'.format(self.name)
        token = getattr(ctx, attr, None)
        if token:
            return token

        if session.get("user"):
            token = OAuth2Token.get(name=self.name, user_id=session["user"]["__id"])
            if not token:
                raise LoginRequiredError("")
        else:
            access_token = self.parse_access_token()
            if not access_token:
                raise LoginRequiredError(
                    "No user session active or access token provided.")
            token = OAuth2Token.get(access_token=access_token)
            if not token:
                raise LoginRequiredError("Access token is invalid.")
        if token.is_active:
            return token
        else:
            new_token = self.refresh_token(token.refresh_token)
            return OAuth2Token.save(name=self.name,
                                    user_id=token.user_id,
                                    **new_token)

    @token.setter
    def token(self, token):
        ctx = _app_ctx_stack.top
        attr = 'authlib_oauth_token_{}'.format(self.name)
        setattr(ctx, attr, token)

    def refresh_token(self, refresh_token=None):
        """Calls the refresh token endpoint to receive a new auth token.
        """
        metadata = self.load_server_metadata()
        with self._get_oauth_client(**metadata) as client:
            new_token = client.refresh_token(metadata['token_endpoint'],
                                             refresh_token=refresh_token)
            if new_token.get('error') == 'invalid_grant':
                raise LoginRequiredError('Refresh token is expired.')
            return new_token

    def handle_auth_token(self, token, user_id_field="sub"):
        """Convenience method used post-authentication when an auth token is received
        from the auth provider. Parses token, saves it in the database, and initializes
        user session.
        """
        LOGGER.debug(f"Token Info: {token}")
        user = self.parse_id_token(token)
        LOGGER.debug(f"User Info: {user}")
        user_id = user.get(user_id_field)
        if not user_id:
            raise BadRequest(
                "Make sure to set the proper 'FLASK_OIDC_USER_ID_FIELD' env variable "
                f"to match with your OIDC Provider. '{user_id_field}' is not present in the "
                f"response from OIDC Provider. Available Keys are: ({', '.join(user.keys())})"
            )
        OAuth2Token.save(name=self.name, user_id=user_id, **token)
        session["user"] = user
        session["user"]["__id"] = user_id
        session.permanent = True
        return user

    @staticmethod
    def parse_access_token():
        if "Authorization" in request.headers and \
                request.headers["Authorization"].startswith("Bearer "):
            return request.headers["Authorization"].split(None, 1)[1].strip()
        return None
