from .service import Service, ServiceManagementClient
from terrene.utils.exceptions import UnknownError
import requests


class Application(Service):

    def deploy(self):
        """
        re-deploys the cluster
        
        Returns: None
        
        Raises:
            UnknownError: if deployment didn't successfully start
        """
        res = requests.get(
            self._path + "deploy/",
            headers=self._headers
        )

        if res.status_code != 200:
            raise UnknownError


class ApplicationManagementClient(ServiceManagementClient):

    _namespace = "applications"
    _resource_class = Application
