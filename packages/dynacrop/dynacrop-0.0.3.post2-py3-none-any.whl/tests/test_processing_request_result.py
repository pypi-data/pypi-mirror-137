import pytest
import numpy as np  # type: ignore
import geopandas as gpd  # type: ignore
import os

from dynacrop import (Observation, FieldZonation,
                      FieldZonationByMedian)


def mock_get_content(mocked_result_path):
    with open(mocked_result_path, 'rb') as bf:
        return bf.read()


@pytest.fixture(autouse=True)
def rasterprocessingrequest_result_mocker(mocker, mocked_result_path):
    mocker.patch(
        'dynacrop.processing_request_base.RasterProcessingRequest' +
        '._get_content',
        return_value=mock_get_content(
            os.path.join('mocks', mocked_result_path)
        )
    )


@pytest.mark.parametrize(
    'path, apiobject', [
        ('mocked_observation.json', Observation),
        ('mocked_field_zonation.json', FieldZonation),
        ('mocked_field_zonation_by_median.json', FieldZonationByMedian),
    ]
)
class TestRasterProcessingRequestResult:
    # NOTE Only observation bytestring results are used. The principle must
    # be same since as_array is a common method for all children of
    # RasterProcessingRequest. [DELETE]
    @pytest.mark.parametrize('mocked_result_path', [
            'mocked_observation_raw_result'
        ]
    )
    def test_rpr_as_array(self, mocked_apiobject):
        assert isinstance(mocked_apiobject.as_array(), np.ndarray)

    @pytest.mark.parametrize('mocked_result_path', [
            'mocked_observation_shapefile_result'
        ]
    )
    def test_rpr_as_geodataframe(self, mocked_apiobject):
        assert isinstance(
            mocked_apiobject.as_geodataframe(),
            type(gpd.GeoDataFrame())
        )

    @pytest.mark.parametrize('mocked_result_path', [
            'mocked_observation_frequencies_result'
        ]
    )
    def test_rpr_frequencies(self, mocked_apiobject):
        assert isinstance(mocked_apiobject.get_frequencies(), dict)


@pytest.mark.parametrize(
    'path, apiobject, mocked_result_path', [
        (
            'mocked_observation.json',
            Observation,
            'mocked_observation_stats_result'
        )
    ]
)
def test_observation_stats(mocked_apiobject):
    result = mocked_apiobject._get_stats()
    assert isinstance(result, dict)
    assert all([stat in result.keys() for stat
                in ['mean', 'median', 'min', 'max', 'sd', 'percentiles']])

# noqa
# NOTE I feel like we do not need to test JSONProcessingRequest as there's
# nothing left up on SDK.

# @pytest.fixture()
# def jsonprocessingrequest_result_mocker(mocker, mocked_result_path):
#     mocker.patch(
#         'dynacrop.processing_request_base.JSONProcessingRequest' +
#         '.get_json',
#         return_value=mocked_apiobject._data['result']['time_series']
#     )
# @pytest.mark.parametrize(
#     'path, apiobject',
#     [('mocked_time_series.json', TimeSeries)]
# )
# def test_time_series_result(mocked_apiobject):
#     result = mocked_apiobject.get_json()
#     assert isinstance(result, dict)
#     assert ['dates', 'values'] in result.keys
