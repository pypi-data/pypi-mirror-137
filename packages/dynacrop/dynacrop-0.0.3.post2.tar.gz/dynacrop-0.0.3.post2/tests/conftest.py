import json
import pytest # noqa
import os


def get_mocked_data(path):
    with open(os.path.join('mocks', path)) as md:
        return json.load(md)


@pytest.fixture(autouse=True)
def apiobject_mocker(mocker, path):
    mocker.patch(
        'dynacrop.api_handles.APIObject.refresh',
        return_value=None
    )

    mocker.patch(
        'dynacrop.api_handles.RequestsHelper.get',
        return_value=get_mocked_data(path)
    )

    mocker.patch(
        'dynacrop.api_handles.RequestsHelper.patch',
        return_value=None
    )

    mocker.patch(
        'dynacrop.api_handles.RequestsHelper.list',
        return_value=get_mocked_data(path)
    )


@pytest.fixture()
def mocked_apiobject(apiobject):
    return apiobject.get(1)


@pytest.fixture()
def mocked_apiobject_list(apiobject):
    return apiobject.list()
