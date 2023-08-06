from amaz3dpy.models import LoginOutput, LoginInput
from amaz3dpy.webapiclients.gqlhttpclient import GQLHttpClientError, GQLHttpClient
from gql import gql
import jwt
from appdirs import *
import json
import os

class Auth():

    def __init__(self, url = "amaz3d_backend.adapta.studio", use_ssl=True, strict_url=False, credentials=False, refresh_token=True):
        
        self.clear()
        self.__url = url + '/graphql' if not strict_url else url
        self.__use_ssl = use_ssl
        self.__authenticated = False
        self.__auth_message = None

        appname = "amaz3dpy"
        appauthor = "Adapta Studio"
        app_path = user_data_dir(appname, appauthor)
        self.__credentials_path = os.path.join(app_path, "credentials.json")
        self.__refresh_token_path = os.path.join(app_path, "refresh_token.json")
        os.makedirs(os.path.dirname(self.__credentials_path), exist_ok=True)
        os.makedirs(os.path.dirname(self.__refresh_token_path), exist_ok=True)

        self.__save_credentials = credentials
        self.__save_refresh_token = refresh_token

        if credentials:
            try:
                self.load_credentials()
            except:
                pass

        if refresh_token:
            try:
                self.load_refresh_token()
            except:
                pass

    def clear_configs(self):
        try:
            os.remove(self.__credentials_path) 
        except:
            pass

        try:
            os.remove(self.__refresh_token_path) 
        except:
            pass

    def clear(self):
        self.__login_input = None
        self.__login_output = None
        
    @property
    def url(self):
        return self.__url

    @property
    def use_ssl(self):
        return self.__use_ssl

    @property
    def token_value(self):
        if self.__login_output:
            return self.__login_output.token

        return None

    @property
    def token(self):

        if self.__login_output:
            if not self._check_token_validation(self.__login_output.token) \
            and not self._check_token_validation(self.__login_output.refreshToken):
                self.refresh_token()
            return self.__login_output.token
        else:
            lo = self.login()
            if lo and lo.token:
                return lo.token
        return None

    @property
    def refresh_token(self):
        if self.login_output:
            return self.login_output.refreshToken

    @property
    def login_input(self):
        return self.__login_input

    @login_input.setter
    def login_input(self, value: str):
        self.__login_input = value

        if self.__save_credentials:
            self.save_credentials()

    @classmethod
    def _check_token_validation(cls, token):
        try:
            jwt.decode(token, options={"verify_signature": False, "verify_exp": True})
            return True
        except jwt.ExpiredSignatureError:
            return False
        except:
            return False

    def save_credentials(self):
        self.__save_credentials = True
        if self.__login_input:
            json.dump(self.__login_input.dict(exclude_unset=True), open(self.__credentials_path, 'w'))

    def save_refresh_token(self):
        self.__save_refresh_token = True
        if self.__login_output:
            json.dump(self.__login_output.dict(exclude_unset=True), open(self.__refresh_token_path, 'w'))

    def load_credentials(self):
        self.__login_input = LoginInput(**json.load(open(self.__credentials_path)))

    def load_refresh_token(self):
        self.__login_output = LoginOutput(**json.load(open(self.__refresh_token_path)))

    def clear_credentials(self):
        try:
            os.remove(self.__credentials_path)
        except:
            pass

    def clear_refresh_token(self):
        try:
            os.remove(self.__refresh_token_path) 
        except:
            pass
    
    def refresh_token(self):

        if self.__login_output is None:
            raise Exception("Refresh token not available")

        query = gql(
            """
            mutation refreshToken($input: RefreshInput!) {
                refreshToken(input: $input) {
                    token
                    refreshToken
                }
            }
            """
        )

        params = {
            "input": {
                "refreshToken": self.__login_output.refreshToken
            }
        }

        try:
            self.__login_output = GQLHttpClient(url=self.url,use_ssl=self.use_ssl).execute(query, params, LoginOutput)

            if self.__save_refresh_token:
                self.save_refresh_token()

            self.__authenticated = True
            self.__auth_message = "Successful"
        except GQLHttpClientError as ex:
            return None

        return self.__login_output

    def login(self):

        query = gql(
            """
            mutation Login($input: LoginInput!) {
                login(input: $input) {
                    token
                    refreshToken
                }
            }
            """
        )

        params = {
            "input": self.__login_input.dict() if self.__login_input is not None else ""
        }

        try:
            self.__login_output = GQLHttpClient(url=self.url,use_ssl=self.use_ssl).execute(query, params, LoginOutput)
            if self.__save_refresh_token:
                self.save_refresh_token()

            self.__authenticated = True
            self.__auth_message = "Successful"
        except GQLHttpClientError as ex:
            return None

        return self.__login_output