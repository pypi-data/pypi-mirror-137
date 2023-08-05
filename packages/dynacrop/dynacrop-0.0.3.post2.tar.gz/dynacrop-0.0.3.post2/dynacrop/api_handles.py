from __future__ import annotations

from time import sleep
from typing import Any, Iterator, Optional, Set, Type

import requests  # noqa

from .config import Config
from .constants import BASEURL
from .exceptions import (APIObjectNotFound, APIRequestNotValid,
                         AuthenticationError, BadGatewayError,
                         HandlingResponseError, MissingID,
                         ServiceNotImplementedError, ServiceUnavailableError,
                         UnexpectedServerError)


class RequestsHelper:
    """Interface for handling requests."""

    @classmethod
    def get(cls, id: str, endpoint: str) -> dict:
        """Creates a GET request for the supplied id and endpoint.

        Args:
            id (str): Used to indentify the endpoint instance.
            endpoint (str): One of the DynaCrop API endpoints.

        Returns:
            dict: Reponse to the request.
        """

        r = requests.get(
            cls.build_url(endpoint, id),
            params={'api_key': Config().api_key})
        return cls.handle_response(r)

    @classmethod
    def patch(cls, id: str, data: dict, endpoint: str) -> dict:
        """Creates a PATCH request for the supplied id, endpoint
    and patch data.

        Args:
            id (str): Used to indentify the endpoint instance.
            data (dict): Used to patch the existing backend data.
            endpoint (str): One of the DynaCrop API endpoints.


        Returns:
            dict: Response to the request with patched data.
        """
        r = requests.patch(
            cls.build_url(endpoint, id),
            params={'api_key': Config().api_key}, data=data)
        return cls.handle_response(r)

    @classmethod
    def post(cls, data: dict, endpoint: str) -> dict:
        """Creates a POST request for the supplied id, endpoint and post data.

        Args:
            id (str): Used to indentify the endpoint instance.
            data (dict): Used to create new instance of the endpoint
            on the backend.
            endpoint (str): One of the DynaCrop API endpoints.


        Returns:
            dict: Response to the request with a new instance
            of endpoint.
        """
        r = requests.post(
            cls.build_url(endpoint),
            params={'api_key': Config().api_key},
            data=data)
        return cls.handle_response(r)

    @classmethod
    def delete(cls, id: str, endpoint: str):
        """Creates a DELETE request for the supplied endpoint and id.

        Args:
            id (str): Used to indentify the endpoint instance.
            endpoint (str): One of the DynaCrop API endpoints.

        Returns:
            [type]: [description]
        """
        r = requests.delete(
            cls.build_url(endpoint, id),
            params={'api_key': Config().api_key})
        return cls.handle_response(r)

    @classmethod
    def list(
        cls,
        endpoint: Optional[str] = None,
        url: Optional[str] = None
    ) -> dict:
        """Fetches bulk version of an endpoint to return pagination info and
        multiple endpoint results.

        Args:
            endpoint (str): One of the DynaCrop API endpoints. Either endpoint
                or url must be stated.
            url (int): URL to list endpoints. Either endpoint
                or url must be stated.

        Returns:
            dict: Response to the request.
        """
        params: dict = {}

        if endpoint:
            req = cls.build_url(endpoint)
            params = {'api_key': Config().api_key}
        elif url:
            req = url
            params = {}
        else:
            # TODO custom exception
            raise Exception

        r = requests.get(
            req,
            params=params)
        return cls.handle_response(r)

    @classmethod
    def handle_response(cls, response: requests.Response):
        """Handles response from the request methods.

        Args:
            response (dict): Reponse supplied via request methods
            of the RequestHelper class

        Raises:
            APIObjectNotFound: 404 Not Found. Might be a non-existent
                response content or a API-side error.
            APIRequestNotValid: 400 Bad Request. Might be a wrongly
                defined request.
            UnexpectedServerError: 500 Internal Server Error. Might be an API
                error that can only be resolved on server side.
            ServiceNotImplementedError: 501 Not Implemented. The request was
                not recognized by the API server. Might be implemented
                in the future.
            BadGatewayError: 502 Bad Gateway. There could have been an error
                beyond the DynaCrop API.
            ServiceUnavailableError: 503 Service Unavailable. The API
                is temporarily unavailable.
            HandlingResponseError: Some other unrecognized error.

        Returns: None
        """
        if response.status_code == 200 or response.status_code == 201:
            return response.json()
        elif response.status_code == 204:
            pass
        elif response.status_code == 401:
            raise AuthenticationError()
        elif response.status_code == 404:
            raise APIObjectNotFound(response.url)
        elif response.status_code == 400:
            raise APIRequestNotValid(response.json())
        elif response.status_code == 500:
            raise UnexpectedServerError
        elif response.status_code == 501:
            raise ServiceNotImplementedError
        elif response.status_code == 502:
            raise BadGatewayError
        elif response.status_code == 503:
            raise ServiceUnavailableError
        else:
            raise HandlingResponseError

    @classmethod
    def build_url(cls, *args: Optional[str]) -> str:
        """Builds internet url based on parameters

        Returns:
            str: Built URL.
        """
        return '/'.join([BASEURL] + [str(x) for x in args])


class APIObject:
    """Metaclass for various endpoints of the API."""
    _editable_attrs: Set[Any] = set()
    _endpoint: str = ""
    _object_attrs: Set = {'_data'}

    def __init__(self, id: Optional[int] = None, ext_data: dict = None):
        """Constructs an API object.

        Args:
            id (str): ID of an endpoint request.
        """
        self._data: dict = {}
        if ext_data:
            self._data = ext_data
        else:
            self._data = {'id': str(id) if id else ''}
            self.refresh()

    def __dir__(self) -> list:
        return list(self._data.keys())

    def __getattr__(self, item: str) -> Any:
        """An override for getattr.

        Args:
            item (str): Attribute to be found from the object

        Raises:
            AttributeError: If attribute not found.

        Returns:
            Any: APIObject's attribute.
        """

        if self._data['id']:
            try:
                return self._data[item]
            except KeyError:
                raise AttributeError(item)
        else:
            raise Exception(f'{self} has no data.')

    def __setattr__(self, key: str, value: str):
        """An override for setattr.

        Args:
            key (str): The name of the attribute.
            value (str): The value of the attribute.

        Raises:
            AttributeError: If accessed a non-editable attribute .
        """

        if key in self._object_attrs:
            super(APIObject, self).__setattr__(key, value)
        else:
            if key in self._editable_attrs:
                self._data[key] = value
                self._data = RequestsHelper.patch(
                    self.id,
                    {key: self._data[key]
                        for key
                        in self._editable_attrs},
                    self._endpoint)
            else:
                raise AttributeError(key)

    @classmethod
    def get(cls, id: Optional[int] = None) -> APIObject:
        """Acquires APIObject instatiated into one of the DynaCrop API endpoints.

        Args:
            id (int): ID of an endpoint request.

        Returns:
            APIObject: APIObject made to an API endpoint.
        """
        return cls(id)

    @classmethod
    def create(cls, **kwargs) -> APIObject:
        """Creates APIObject later instatiated into one of the DynaCrop API endpoints.

        Args:
            kwargs (Optional[str])

        Returns:
            APIObject: APIObject made to an API endpoint.
        """
        return cls.get(RequestsHelper.post(
            {key: val for key, val in kwargs.items() if val},
            cls._endpoint)['id'])

    def delete(self):
        """Deletes APIObject from the API.
        """
        RequestsHelper.delete(self.id, self._endpoint)
        self._data = {'id': ''}

    @classmethod
    def list(cls) -> Iterator[APIObject]:
        """Fetches APIObjects in bulk as an iterator.

        Returns:
            APIObjectIterator: Iterator of APIObjects.
        """
        return iter(APIObjectIterator(cls))

    def is_ready(self) -> bool:
        """Checks whether the request is ready.

        Returns:
            bool: Is ready statement.
        """
        self.refresh()

        return self._data['status'] != 'created' \
            and self._data['status'] != 'rendering'

    def is_failed(self) -> bool:
        """Checks whether the request failed.

        Returns:
            bool: Failure statement.
        """
        return self._data['status'] == 'error'

    def block_till_completed(self, polling_interval: int = 1):
        """Suspends the code execution until the request response is
    returned as finished/with error/with no data.

        Args:
            polling_interval (int, optional): Time to wait between
            checking iterations. Defaults to 1.
        """
        while not self.is_ready():
            sleep(polling_interval)

    def refresh(self):
        """Updates response data."""
        self._data = RequestsHelper.get(self._data['id'], self._endpoint)
        if 'id' not in self._data:
            raise MissingID

    def __eq__(self, other: object) -> bool:
        """Compares two instantiated endpoints (APIObjects).

        Args:
            other (APIObject): Another APIObject to compare.

        Returns:
            bool: Comparation statement.
        """
        if isinstance(other, APIObject):
            return other.id == self.id
        return NotImplemented

    def __repr__(self) -> str:
        """Returns structured information about APIObject.

        Returns:
            str: Structured information about APIObject.
        """
        if self._data and 'id' in self._data:
            return f"<dynacrop.{self.__class__.__name__} {self._data['id']}>"
        else:
            return f"<dynacrop.{self.__class__.__name__} no_id>"


class APIObjectIterator:
    """Iterator for listing existing APIObjects.
    """
    def __init__(self, cls: Type[APIObject]):
        """Constructs iterator.

        Args:
            cls (APIObject): APIObject for recognizing further iterator
                operations.
        """
        self.cls = cls
        self.object_index = 0
        self.apiobject_list = RequestsHelper.list(
            endpoint=self.cls._endpoint)

    def map_to_correct_instance(self, endpoint_data: dict) -> APIObject:
        """Maps an APIObject (like ProcessingRequest) to a correct child if necessary.

        Args:
            endpoint_data (dict): Data of the API endpoint/object.

        Returns:
            APIObject: Profound APIObject instance.
        """
        from .processing_request_base import ProcessingRequest
        from .sdk import (FieldZonation, FieldZonationByMedian, Observation,
                          TimeSeries)

        pr_map = {
            'observation': Observation,
            'field_zonation': FieldZonation,
            'field_zonation_by_median': FieldZonationByMedian,
            'time_series': TimeSeries
        }

        if self.cls == ProcessingRequest:
            return pr_map[
                    endpoint_data['rendering_type']
                ](ext_data=endpoint_data)
        return self.cls(ext_data=endpoint_data)

    def __iter__(self) -> APIObjectIterator:
        """Returns iterator.

        Returns:
            APIObjectIterator: The iterator.
        """
        return self

    def __next__(self) -> APIObject:
        """Acquires next object on the page within pagination. Automatically
        calls next page if necessary.

        Raises:
            StopIteration: When there are no more results to iterate over.

        Returns:
            APIObject: APIObject made to an API endpoint.
        """
        try:
            endpoint_data = self.apiobject_list['results'][self.object_index]
            self.object_index += 1
            return self.map_to_correct_instance(endpoint_data)
        except IndexError:
            self.object_index = 0
            if 'next' in self.apiobject_list['pagination']:
                self.apiobject_list = RequestsHelper.list(
                    url=self.apiobject_list['pagination']['next']
                )
                endpoint_data = \
                    self.apiobject_list['results'][self.object_index]
                self.object_index += 1
                return self.map_to_correct_instance(endpoint_data)
            else:
                raise StopIteration
