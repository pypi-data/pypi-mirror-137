import pytest

from dynacrop import (ProcessingRequest, Observation, FieldZonation,
                      FieldZonationByMedian)
from dynacrop.api_handles import APIObjectIterator


@pytest.mark.parametrize(
    'path, apiobject', [
        ('mocked_observation.json', Observation)
    ]
)
def test_correct_instance(mocked_apiobject, apiobject):
    assert isinstance(mocked_apiobject, apiobject)


@pytest.mark.parametrize(
    'path, apiobject', [
        ('mocked_observation.json', Observation)
    ]
)
def test_processing_request_has_id(mocked_apiobject):
    assert mocked_apiobject.id


@pytest.mark.parametrize(
    'path, apiobject', [('mocked_observation.json', Observation)]
)
@pytest.mark.parametrize('noneditable_attr', [
    'id',
    'date_from',
    'date_to',
    'value_no_data',
    'value_clouds',
    'result',
    'layer',
    'polygon_id'
])
def test_processing_request_noneditable_attrs(
    mocked_apiobject,
    noneditable_attr
):
    with pytest.raises(AttributeError):
        setattr(mocked_apiobject, noneditable_attr, 'nonsense')


@pytest.mark.parametrize(
    'path, apiobject, noneditable_attr',
    [('mocked_observation.json', FieldZonation, 'number_of_zones')]
)
def test_field_zonation_noneditable_attrs(
    mocked_apiobject,
    noneditable_attr
):
    with pytest.raises(AttributeError):
        setattr(mocked_apiobject, noneditable_attr, 'nonsense')


@pytest.mark.parametrize(
    'path, apiobject, noneditable_attr',
    [('mocked_observation.json', FieldZonationByMedian, 'thresholds')]
)
def test_field_zonation_by_median_noneditable_attrs(
    mocked_apiobject,
    noneditable_attr
):
    with pytest.raises(AttributeError):
        setattr(mocked_apiobject, noneditable_attr, 'nonsense')


@pytest.mark.parametrize(
    'path, apiobject',
    [('mocked_processing_request_list.json', ProcessingRequest)]
)
def test_polygon_list(mocked_apiobject_list):
    assert isinstance(mocked_apiobject_list, APIObjectIterator)
    assert isinstance(next(mocked_apiobject_list), ProcessingRequest)
