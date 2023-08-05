import json
from types import SimpleNamespace

import requests

from ikologikapi.IkologikApiCredentials import IkologikApiCredentials
from ikologikapi.IkologikException import IkologikException
from ikologikapi.domain.Search import Search
from ikologikapi.services.AbstractIkologikService import AbstractIkologikService


class AbstractIkologikCustomerService(AbstractIkologikService):

    def __init__(self, jwtHelper: IkologikApiCredentials):
        super().__init__(jwtHelper)

    # CRUD Actions

    def get_url(self, customer: str):
        pass

    def get_by_id(self, customer: str, id: str) -> object:
        try:
            response = requests.get(
                self.get_url(customer) + f'/{id}',
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
            raise IkologikException("Error while getting customer with id: " + id)

    def list(self, customer: str) -> list:
        try:
            response = requests.get(
                self.get_url(customer),
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
            raise IkologikException("Error while querying list of customers")


    def search(self, customer: str, search: Search) -> list:
        try:
            data = json.dumps(search, default=lambda o: o.__dict__)
            response = requests.post(
                f'{self.get_url(customer)}/search',
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
            raise IkologikException("Error while searching for a customer")

    def create(self, customer: str, o: object) -> object:
        try:
            data = json.dumps(o, default=lambda o: o.__dict__)
            response = requests.post(
                self.get_url(customer),
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
            raise IkologikException("Error while creating a customer")

    def update(self, customer: str, id: str, o: object) -> object:
        try:
            data = json.dumps(o, default=lambda o: o.__dict__)
            response = requests.put(
                f'{self.get_url(customer)}/{id}',
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
            raise IkologikException("Error while updating a customer")

    def delete(self, customer: str, id: str):
        try:
            response = requests.delete(
                f'{self.get_url(customer)}/{id}',
                headers=self.get_headers()
            )
            if response.status_code != 204:
                raise IkologikException("Request returned status " + str(response.status_code))
        except IkologikException as error:
            raise IkologikException("Error while deleting a customer")
        except Exception as ex:
            raise IkologikException("Error while deleting a customer")