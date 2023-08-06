# -*- coding: utf-8 -*-
from chibi_auth0.urls import well_know, user, auth_token, user_info
from chibi_requests.auth import Bearer


class Chibi_auth0:
    def __init__( self, domain, audience, client_id, client_secret ):
        self.domain = domain
        self.audience = audience
        self.client_id = client_id
        self.client_secret = client_secret

    @property
    def well_know( self ):
        return well_know.format( domain=self.domain ).get().native

    @property
    def auth_token( self ):
        return auth_token.format( domain=self.domain )

    def user( self, user_id ):
        url = user.format( domain=self.domain, user_id=user_id )
        url = url + self.client_auth_token
        return url

    def user_info( self, user_id ):
        return self.user( user_id ).get().native

    def user_password_token( self, username, password, scope=None ):
        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "audience": self.audience,
            "grant_type": "password",
            "username": username,
            "password": password,
            "scope": scope,
        }
        response = self.auth_token.post( json=params )
        return response.native

    def user_info( self, access_token, token_type='Bearer' ):
        url = user_info.format( domain=self.domain )
        url.headers[ 'Authorization' ] = f"{token_type} {access_token}"
        response = url.get()
        return response.native

    @property
    def client_auth_token( self ):
        try:
            return self._client_auth_token
        except AttributeError:
            audience = f"https://{self.domain}/api/v2/"
            params = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "audience": audience,
                "grant_type": "client_credentials",
            }
            response = self.auth_token.post( json=params )
            if not response.ok:
                raise NotImplementedError(
                    f"params\n{params}headers\n{response.headers}\n"
                    f"content\n{response.content}" )
            self._client_auth_token = Bearer(
                token=response.native.access_token )
            return self._client_auth_token

    @property
    def _info( self ):
        if not self.url:
            raise NotImplementedError(
                f"the class {self} no have url" )
        return self.__url_format().get().native

    def __url_format( self ):
        return self.url
