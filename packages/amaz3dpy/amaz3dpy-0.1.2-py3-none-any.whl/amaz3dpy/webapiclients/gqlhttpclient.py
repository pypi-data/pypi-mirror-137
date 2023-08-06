from ast import IsNot
from gql import Client
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.exceptions import TransportQueryError

class GQLHttpClientError(Exception):
    pass

class GQLHttpClient():

    def __init__(self, token=None, url = None, use_ssl = True):
        headers = {}
        protocol = "https://" if use_ssl else "http://"

        if token:
            headers['Authorization'] = 'Bearer ' + token

        self.__transport = AIOHTTPTransport(url=protocol+url, headers=headers, timeout=120, ssl_close_timeout=120)
        self.__client = Client(transport=self.__transport, execute_timeout=1200)

    def execute(self, query: str, params: dict, model=None, upload_files=False):
        try:
            result = self.__client.execute(query, variable_values=params, upload_files=upload_files)

            if len(result) == 1 and model is not None:
                root = list(result.keys())[0]
                return model(**result[root])

            return result

        except TransportQueryError as ex:
            raise GQLHttpClientError(ex.errors[0]['message'])