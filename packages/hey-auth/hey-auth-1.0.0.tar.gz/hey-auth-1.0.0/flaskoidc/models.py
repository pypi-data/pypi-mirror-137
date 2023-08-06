import logging
import time
from sqlalchemy import Column, Integer, String, TEXT
from flask import current_app as app

LOGGER = logging.getLogger(f"flaskoidc.{__name__}")


class OAuth2Token(app.db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(String(320), nullable=False)
    name = Column(String(20), nullable=False)

    access_token = Column(TEXT, nullable=False)
    expires_in = Column(Integer, default=0)
    scope = Column(String(320), default=0)
    token_type = Column(String(20))
    refresh_token = Column(TEXT)
    expires_at = Column(Integer, default=0)

    def to_token(self):
        return dict(
            access_token=self.access_token,
            expires_in=self.expires_in,
            scope=self.scope,
            token_type=self.token_type,
            refresh_token=self.refresh_token,
            expires_at=self.expires_at,
        )

    @property
    def is_active(self):
        return self.expires_at > round(time.time())

    @staticmethod
    def save(**kwargs):
        OAuth2Token.delete(name=kwargs['name'], user_id=kwargs['user_id'])
        token = OAuth2Token(**OAuth2Token.filter_token(kwargs))
        app.db.session.add(token)
        app.db.session.commit()
        return token

    @staticmethod
    def get(**kwargs):
        return OAuth2Token.query.filter_by(**kwargs).first()

    @staticmethod
    def delete(**kwargs):
        OAuth2Token.query.filter_by(**kwargs).delete()
        app.db.session.commit()

    @staticmethod
    def all():
        return OAuth2Token.query.all()

    @staticmethod
    def filter_token(token):
        return {_key: token.get(_key) for _key in token.keys() if _key in OAuth2Token.__dict__.keys()}
