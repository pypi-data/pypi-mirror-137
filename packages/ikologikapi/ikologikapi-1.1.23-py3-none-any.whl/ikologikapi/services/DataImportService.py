import json
from types import SimpleNamespace

import requests

from ikologikapi.IkologikApiCredentials import IkologikApiCredentials
from ikologikapi.IkologikException import IkologikException
from ikologikapi.domain.Search import Search
from ikologikapi.services.AbstractIkologikInstallationService import AbstractIkologikInstallationService


class DataImportService(AbstractIkologikInstallationService):

    def __init__(self, jwtHelper: IkologikApiCredentials):
        super().__init__(jwtHelper)

    # CRUD Actions

    def get_url(self, customer, installation, data_import_type):
        return f'{self.jwtHelper.get_url()}/api/v2/customer/{customer}/installation/{installation}/dataimporttype/{data_import_type}/dataimport'

    def list(self, customer: str, installation: str, data_import_type: str, search) -> list:
        try:
            response = requests.get(
                f'{self.get_url(customer, installation, data_import_type)}/search',
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
            raise IkologikException("Error while querying list of the dataimport")

    def get_by_id(self, customer: str, installation: str, data_import_type: str, id: str) -> object:
        try:
            response = requests.get(
                self.get_url(customer, installation, data_import_type) + f'/{id}',
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
            raise IkologikException("Error while getting the dataimport by id")

    def search(self, customer: str, installation: str, data_import_type: str, search) -> list:
        try:
            data = json.dumps(search, default=lambda o: o.__dict__)
            response = requests.post(
                f'{self.get_url(customer, installation, data_import_type)}/search',
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
            raise IkologikException("Error while searching for dataimport")

    def create(self, customer: str, installation: str, data_import_type: str, o: object) -> object:
        try:
            data = json.dumps(o, default=lambda o: o.__dict__)
            response = requests.post(
                self.get_url(customer, installation, data_import_type),
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
            raise IkologikException("Error while creating dataimport")

    def update(self, customer: str, installation: str, data_import_type: str, o: object):
        try:
            data = json.dumps(o, default=lambda o: o.__dict__)
            response = requests.put(
                f'{self.get_url(customer, installation, data_import_type)}/{o.id}',
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
            raise IkologikException("Error while updating dataimport")

    def delete(self, customer: str, installation: str, data_import_type: str, id: str):
        try:
            response = requests.delete(
                f'{self.get_url(customer, installation, data_import_type)}/{id}',
                headers=self.get_headers()
            )
            if response.status_code != 204:
                raise IkologikException("Request returned status " + str(response.status_code))
        except IkologikException as error:
            raise IkologikException("Error while deleting dataimport")
        except Exception as ex:
            raise IkologikException("Error while deleting dataimport")

    def update_status(self, customer: str, installation: str, data_import_type: str, id: str, status) -> object:
        try:
            response = requests.put(
                f'{self.get_url(customer, installation, data_import_type)}/{id}/status',
                data=status,
                headers=self.get_headers_update_status()
            )
            if response.status_code == 200:
                result = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
                return result
            else:
                raise IkologikException("Request returned status " + str(response.status_code))
        except IkologikException as ex:
            raise ex
        except Exception as ex:
            raise IkologikException("Error while updating the status for the dataimport")

    def update_error(self, customer: str, installation: str, data_import_type: str, id: str, error) -> object:
        try:
            response = requests.put(
                f'{self.get_url(customer, installation, data_import_type)}/{id}/error',
                data=error,
                headers=self.get_headers_update_status()
            )
            if response.status_code == 200:
                result = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
                return result
            else:
                raise IkologikException("Request returned status " + str(response.status_code))
        except IkologikException as ex:
            raise ex
        except Exception as ex:
            raise IkologikException("Error while updating error for dataimport")

    def get_headers_update_status(self):
        headers = {
            'Content-Type': 'text/plain',
            'Authorization': f'Bearer {self.jwtHelper.get_jwt()}'
        }

        return headers


    def get_by_name(self, customer: str, installation: str, name):
        search = Search()
        search.add_filter = ("name", "EQ", [name])
        search.add_order("name", "ASC")

        # Query
        result = self.search(customer, installation, search)
        if result and len(result) == 1:
            return result[0]
        else:
            return None
