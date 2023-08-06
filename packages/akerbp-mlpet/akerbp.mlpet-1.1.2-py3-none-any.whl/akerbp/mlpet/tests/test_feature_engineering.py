# ONLY testing one function from feature_engineering. Would be good to expand this
# if we have some spare time in a sprint
import pytest
from pandas.testing import assert_frame_equal

from akerbp.mlpet import feature_engineering
from akerbp.mlpet.tests.data import (
    FORMATION_DF,
    FORMATION_TOPS_MAPPER,
    VERTICAL_DF,
    VERTICAL_DEPTHS_MAPPER,
)
from cognite.client import CogniteClient

client = CogniteClient(client_name="test", project="akbp-subsurface")


def test_add_formation_tops_using_mapper():
    df_with_tops = feature_engineering.add_formation_tops_label(
        FORMATION_DF[["DEPTH", "well_name"]],
        formation_tops_mapper=FORMATION_TOPS_MAPPER,
        id_column="well_name",
    )
    # Sorting columns because column order is not so important
    assert_frame_equal(df_with_tops.sort_index(axis=1), FORMATION_DF.sort_index(axis=1))


def test_add_formation_tops_using_client():
    df_with_tops = feature_engineering.add_formation_tops_label(
        FORMATION_DF[["DEPTH", "well_name"]],
        id_column="well_name",
        client=client,
    )
    assert_frame_equal(df_with_tops.sort_index(axis=1), FORMATION_DF.sort_index(axis=1))


def test_add_formation_tops_raises_exception_if_no_client_nor_mapping_is_provided():
    with pytest.raises(
        Exception,
        match="Neither a formation tops mapping nor cognite client is provided. Not able to add formation tops to dataset",
    ):
        _ = feature_engineering.add_formation_tops_label(
            FORMATION_DF[["DEPTH", "well_name"]],
            id_column="well_name",
        )


def test_add_vertical_depths_using_mapper():
    df_with_vertical_depths = feature_engineering.add_vertical_depths(
        VERTICAL_DF[["DEPTH", "well_name"]],
        vertical_depths_mapper=VERTICAL_DEPTHS_MAPPER,
        id_column="well_name",
        md_column="DEPTH",
    )

    assert_frame_equal(
        df_with_vertical_depths.sort_index(axis=1), VERTICAL_DF.sort_index(axis=1)
    )


def test_add_vertical_depths_using_client():
    df_with_vertical_depths = feature_engineering.add_vertical_depths(
        VERTICAL_DF[["DEPTH", "well_name"]],
        id_column="well_name",
        md_column="DEPTH",
        client=client,
    )

    assert_frame_equal(
        df_with_vertical_depths.sort_index(axis=1), VERTICAL_DF.sort_index(axis=1)
    )


def test_add_vertical_depths_raises_expection_if_no_client_nor_mapping_is_provided():
    with pytest.raises(
        Exception,
        match="Neither a vertical depths mapping nor a cognite client is provided. Not able to add vertical depths to dataset",
    ):
        _ = feature_engineering.add_vertical_depths(
            VERTICAL_DF[["DEPTH", "well_name"]],
            id_column="well_name",
            md_column="DEPTH",
        )
