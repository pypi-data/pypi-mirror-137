import json
from types import SimpleNamespace

import requests

from ikologikapi.IkologikApiCredentials import IkologikApiCredentials
from ikologikapi.IkologikException import IkologikException
from ikologikapi.services.AbstractIkologikInstallationService import AbstractIkologikInstallationService


class DashboardWidgetService(AbstractIkologikInstallationService):

    def __init__(self, jwtHelper: IkologikApiCredentials):
        super().__init__(jwtHelper)

    # CRUD Actions

    def get_url(self, customer: str, installation: str, dashboard: str):
        return f'{self.jwtHelper.get_url()}/api/v2/customer/{customer}/installation/{installation}/dashboard/{dashboard}/widget'

    def list(self, customer: str, installation: str, dashboard: str, search) -> list:
        try:
            response = requests.get(
                f'{self.get_url(customer, installation, dashboard)}/search',
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
            raise IkologikException("Error while listing a dashboardwidget")

    def search(self, customer: str, installation: str, dashboard: str, search) -> list:
        try:
            data = json.dumps(search, default=lambda o: o.__dict__)
            response = requests.post(
                f'{self.get_url(customer, installation, dashboard)}/search',
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
            raise IkologikException("Error while searching for a dashboardwidget")

    def create(self, customer: str, installation: str, dashboard: str, o: object) -> object:
        try:
            data = json.dumps(o, default=lambda o: o.__dict__)
            response = requests.post(
                self.get_url(customer, installation, dashboard),
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
            raise IkologikException("Error while creating a dashboardwidget")

    def update(self, customer: str, installation: str, dashboard: str, o: object):
        try:
            data = json.dumps(o, default=lambda o: o.__dict__)
            response = requests.put(
                f'{self.get_url(customer, installation, dashboard)}/{o.id}',
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
            raise IkologikException("Error while updating a dashboardwidget")

    def delete(self, customer: str, installation: str, dashboard: str, id: str):
        try:
            response = requests.delete(
                f'{self.get_url(customer, installation, dashboard)}/{id}',
                headers=self.get_headers()
            )
            if response.status_code != 204:
                raise IkologikException("Request returned status " + str(response.status_code))
        except IkologikException as error:
            raise IkologikException("Error while deleting a dashboardwidget")
        except Exception as ex:
            raise IkologikException("Error while deleting a dashboardwidget")