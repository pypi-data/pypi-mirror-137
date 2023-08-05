import pytest

from dynacrop.api_handles import APIObjectIterator
from dynacrop import Polygon


@pytest.mark.parametrize(
    'path, apiobject', [
        ('mocked_polygon.json', Polygon),
    ]
)
class TestMockedPolygon:
    def test_correct_instance(self, mocked_apiobject, apiobject):
        assert isinstance(mocked_apiobject, apiobject)

    def test_polygon_has_id(self, mocked_apiobject):
        assert mocked_apiobject.id

    @pytest.mark.parametrize('noneditable_attr', [
        'id',
        'geometry',
        'area',
        'last_valid_observation',
        'valid_observations',
        'cloud_cover_percent',
        'last_updated']
    )
    def test_polygon_noneditable_attrs(
        self,
        mocked_apiobject,
        noneditable_attr
    ):
        with pytest.raises(AttributeError):
            setattr(mocked_apiobject, noneditable_attr, 'nonsense')


@pytest.mark.parametrize(
    'path, apiobject', [('mocked_polygon_list.json', Polygon)]
)
def test_polygon_list(mocked_apiobject_list):
    assert isinstance(mocked_apiobject_list, APIObjectIterator)
    assert isinstance(next(mocked_apiobject_list), Polygon)
