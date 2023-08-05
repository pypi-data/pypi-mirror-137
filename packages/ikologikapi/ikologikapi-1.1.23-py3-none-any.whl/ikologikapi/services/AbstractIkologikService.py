import json
from types import SimpleNamespace

import requests

from ikologikapi.IkologikApiCredentials import IkologikApiCredentials
from ikologikapi.IkologikException import IkologikException
from ikologikapi.domain.Search import Search


class AbstractIkologikService:

    def __init__(self, jwtHelper: IkologikApiCredentials):
        self.jwtHelper = jwtHelper

    # CRUD Actions

    def get_headers(self, default_headers=None):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.jwtHelper.get_jwt()}'
        }
        if default_headers is not None:
            # headers.update((k, v) for k, v in default_headers.items() if v is not None)
            headers.update(default_headers)
        return headers

    def get_url(self):
        pass

    def get_by_id(self, id: str) -> object:
        try:
            response = requests.get(
                self.get_url() + f'/{id}',
                headers=self.get_headers()
            )
            if response.status_code == 200:
                result = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
                return result
            else:
                raise IkologikException("Request returned status " + str(response.status_code))
        except IkologikException as ex:
            raise ex
        except Exception as ex:
            raise IkologikException("Error while getting by id")

    def list(self) -> list:
        try:
            response = requests.get(
                self.get_url(),
                headers=self.get_headers()
            )
            if response.status_code == 200:
                result = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
                return result
            else:
                raise IkologikException("Request returned status " + str(response.status_code))
        except IkologikException as ex:
            raise ex
        except Exception as ex:
            raise IkologikException("Error while querying list")

    def search(self, search: Search) -> list:
        try:
            data = json.dumps(search, default=lambda o: o.__dict__)
            response = requests.post(
                f'{self.get_url()}/search',
                data=data,
                headers=self.get_headers()
            )
            if response.status_code == 200:
                result = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
                return result
            else:
                raise IkologikException("Request returned status " + str(response.status_code))
        except IkologikException as ex:
            raise ex
        except Exception as ex:
            raise IkologikException("Error while searching")

    def create(self, o: object) -> object:
        try:
            data = json.dumps(o, default=lambda o: o.__dict__)
            response = requests.post(
                self.get_url(),
                data=data,
                headers=self.get_headers()
            )
            if response.status_code == 201:
                result = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
                return result
            else:
                raise IkologikException("Request returned status " + str(response.status_code))
        except IkologikException as ex:
            raise ex
        except Exception as ex:
            raise IkologikException("Error while creating")

    def update(self, id: str, o: object) -> object:
        try:
            data = json.dumps(o, default=lambda o: o.__dict__)
            response = requests.put(
                f'{self.get_url()}/{id}',
                data=data,
                headers=self.get_headers()
            )
            if response.status_code == 200:
                result = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
                return result
            else:
                raise IkologikException("Request returned status " + str(response.status_code))
        except IkologikException as ex:
            raise ex
        except Exception as ex:
            raise IkologikException("Error while updating")

    def delete(self, id: str):
        try:
            response = requests.delete(
                f'{self.get_url()}/{id}',
                headers=self.get_headers()
            )
            if response.status_code != 204:
                raise IkologikException("Request returned status " + str(response.status_code))
        except IkologikException as error:
            raise IkologikException("Error while deleting installation")
        except Exception as ex:
            raise IkologikException("Error while deleting")
