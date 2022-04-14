from typing import Sequence, Any


class Options:
    def __init__(self, name: str, values: Sequence):
        self.name = name
        self.values = values

    def validate(self, value: Any) -> bool:
        if value not in self.values:
            valid = "\n- ".join(self.values)
            raise ValueError(
                f"'{value}' is not a valid {self.name}, "
                + f"please choose from one of the following:\n- {valid}"
            )
        return True


correlation_methods = Options(
    "Correlation Method",
    (
        "RoadLink_TOID_TopographicArea_TOID_2",
        "Street_USRN_TopographicArea_TOID_4",
        "BLPU_UPRN_TopographicArea_TOID_5",
        "RoadLink_TOID_Road_TOID_7",
        "RoadLink_TOID_Street_USRN_8",
        "BLPU_UPRN_RoadLink_TOID_9",
        "Road_TOID_Street_USRN_10",
        "BLPU_UPRN_Street_USRN_11",
        "ORRoadLink_GUID_RoadLink_TOID_12",
        "ORRoadNode_GUID_RoadLink_TOID_13",
    ),
)

identifier_types = Options("Identifier Type", ("TOID", "UPRN", "USRN", "GUID"))

feature_types = Options(
    "Feature Type",
    (
        "TopographicArea",
        "RoadLink",
        "Road",
        "BLPU",
        "Street",
        "ORRoadNode",
        "ORRoadLink",
    ),
)
