from cognite.client import CogniteClient

from akerbp.mlpet import utilities as utils
from akerbp.mlpet.tests.data import FORMATION_TOPS_MAPPER, VERTICAL_DEPTHS_MAPPER

CLIENT = CogniteClient(
    client_name="test",
    project="akbp-subsurface",
)
WELL_NAMES = ["25/10-10"]


def test_get_formation_tops():
    formation_tops_mapper = utils.get_formation_tops(WELL_NAMES, CLIENT)
    assert formation_tops_mapper == FORMATION_TOPS_MAPPER


def test_get_vertical_depths():
    retrieved_vertical_depths = utils.get_vertical_depths(WELL_NAMES, CLIENT)
    # empty_queries should be an empty list for the provided WELL_NAMES
    assert retrieved_vertical_depths == VERTICAL_DEPTHS_MAPPER
