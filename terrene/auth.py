from .api import CoreAPI, CoreAPIMixin, BaseModel, BaseModelManager, BaseConnector
from .config import api
from . import access_key

import coreapi
import os


class User(BaseModel):
    def add_role(self, role):
        return self.act(['roles', 'create'], {
            'object_id': self.object_id, 'role': role})

    def remove_role(self, role):
        return self.act(['roles', 'partial_update'], {
            'object_id': self.object_id, 'role': role})

    def reset_secret_key(self):
        return self.act(['reset_secret_key'], {
            'object_id': self.object_id})

    def set_password(self, new_password, old_password):
        return self.act(['set_password'], {
            'object_id': self.object_id, 'new_password': new_password,
            'old_password': old_password})


class UserManager(BaseModelManager):
    model = User
    namespace = ['users']
    credentials = None

    @property
    def current_user(self):
        return BaseConnector.current_user

    def create(self, params):
        # update the coreapi attribute and credentials attribute to
        # authenticate the newly created user
        user = self.act(['create'], params)
        EmailPasswordCredentials(
            email=params['email'], password=params['password'])
        return self.model(
            user['object_id'], self.namespace, self.coreapi)


class BaseCredentials(BaseConnector):
    namespace = ['users', 'actions', 'login']

    def __init__(self, *args, **kwargs):
        BaseConnector.coreapi = CoreAPI()
        object_id = self._authenticate(*args, **kwargs)

        # attempt to update the coreapi document, and client with the authenticated
        # headers created by the _authenticate method
        BaseConnector.coreapi.client = coreapi.Client(
            transports=[coreapi.transports.HTTPTransport(
                headers=self.headers)])
        BaseConnector.coreapi.document = BaseConnector.coreapi.client.get(api() + '/schema/')

        # retrieve current_user
        if object_id is not None:
            BaseConnector.current_user = User(object_id, UserManager.namespace, BaseConnector.coreapi)

    def _authenticate(self, *args, **kwargs):
        raise NotImplementedError()


class EmailPasswordCredentials(BaseCredentials):
    def _authenticate(self, *args, **kwargs):
        for kwarg in ['email', 'password']:
            if kwargs.get(kwarg, None) is None:
                raise AssertionError(
                    "{} kwarg is required for all the UserPassCredentials instances.".format(
                        kwarg))
        results = self.act(['obtain_token'], {
            'email': kwargs.get('email'), 'password': kwargs.get('password')})
        self.headers['Authorization'] = 'JWT {}'.format(results['token'])
        print('Account verified through email and password')
        return results['user']['object_id']


class TokenCredential(BaseCredentials):
    def _authenticate(self, *args, **kwargs):
        if access_key is None:
            raise AssertionError(
                "token kwarg is required for all the TokenCredential instances.")
        results = self.act(['verify_token'], {
            'token': access_key})
        self.headers['Authorization'] = 'JWT {}'.format(results['token'])
        print('Account verified through JWT')
        return None
