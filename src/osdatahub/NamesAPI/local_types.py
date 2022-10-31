from collections import namedtuple
from collections.abc import Iterable
from typing import Union

Local_Type = namedtuple("LocalType", "Type local_type")

LOCAL_TYPE = {
    "airfield": Local_Type("transportNetwork", "Airfield"),
    "airport": Local_Type("transportNetwork", "Airport"),
    "bay": Local_Type("hydrography", "Bay"),
    "beach": Local_Type("landcover", "Beach"),
    "bus_station": Local_Type("transportNetwork", "Bus_Station"),
    "channel": Local_Type("hydrography", "Channel"),
    "chemical_works": Local_Type("other", "Chemical_Works"),
    "cirque_or_hollow": Local_Type("landform", "Cirque_Or_Hollow"),
    "city": Local_Type("populatedPlace", "City"),
    "cliff_or_slope": Local_Type("landform", "Cliff_Or_Slope"),
    "coach_station": Local_Type("transportNetwork", "Coach_Station"),
    "coastal_headland": Local_Type("landform", "Coastal_Headland"),
    "electricity_distribution": Local_Type("other", "Electricity_Distribution"),
    "electricity_production": Local_Type("other", "Electricity_Production"),
    "estuary": Local_Type("hydrography", "Estuary"),
    "further_education": Local_Type("other", "Further_Education"),
    "gas_distribution_or_storage": Local_Type("other", "Gas_Distribution_or_Storage"),
    "group_of_islands": Local_Type("landform", "Group_Of_Islands"),
    "hamlet": Local_Type("populatedPlace", "Hamlet"),
    "harbour": Local_Type("transportNetwork", "Harbour"),
    "helicopter_station": Local_Type("transportNetwork", "Helicopter_Station"),
    "heliport": Local_Type("transportNetwork", "Heliport"),
    "higher_or_university_education": Local_Type("other", "Higher_or_University_Education"),
    "hill_or_mountain": Local_Type("landform", "Hill_Or_Mountain"),
    "hill_or_mountain_ranges": Local_Type("landform", "Hill_Or_Mountain_Ranges"),
    "hospice": Local_Type("other", "Hospice"),
    "hospital": Local_Type("other", "Hospital"),
    "inland_water": Local_Type("hydrography", "Inland_Water"),
    "island": Local_Type("landform", "Island"),
    "medical_care_accommodation": Local_Type("other", "Medical_Care_Accommodation"),
    "named_road": Local_Type("transportNetwork", "Named_Road"),
    "non_state_primary_education": Local_Type("other", "Non_State_Primary_Education"),
    "non_state_secondary_education": Local_Type("other", "Non_State_Secondary_Education"),
    "numbered_road": Local_Type("transportNetwork", "Numbered_Road"),
    "oil_distribution_or_storage": Local_Type("other", "Oil_Distribution_or_Storage"),
    "oil_refining": Local_Type("other", "Oil_Refining"),
    "oil_terminal": Local_Type("other", "Oil_Terminal"),
    "other_coastal_landform": Local_Type("landform", "Other_Coastal_Landform"),
    "other_landcover": Local_Type("landcover", "Other_Landcover"),
    "other_landform": Local_Type("landform", "Other_Landform"),
    "other_settlement": Local_Type("populatedPlace", "Other_Settlement"),
    "passenger_ferry_terminal": Local_Type("transportNetwork", "Passenger_Ferry_Terminal"),
    "port_consisting_of_docks_and_nautical_berthing": Local_Type("transportNetwork",
                                                                 "Port_Consisting_of_Docks_and_Nautical_Berthing"),
    "postcode": Local_Type("other", "Postcode"),
    "primary_education": Local_Type("other", "Primary_Education"),
    "railway": Local_Type("transportNetwork", "Railway"),
    "railway_station": Local_Type("transportNetwork", "Railway_Station"),
    "road_user_services": Local_Type("transportNetwork", "Road_User_Services"),
    "sea": Local_Type("hydrography", "Sea"),
    "secondary_education": Local_Type("other", "Secondary_Education"),
    "section_of_named_road": Local_Type("transportNetwork", "Section_Of_Named_Road"),
    "section_of_numbered_road": Local_Type("transportNetwork", "Section_Of_Numbered_Road"),
    "special_needs_education": Local_Type("other", "Special_Needs_Education"),
    "spot_height": Local_Type("landform", "Spot_Height"),
    "suburban_area": Local_Type("populatedPlace", "Suburban_Area"),
    "tidal_water": Local_Type("hydrography", "Tidal_Water"),
    "town": Local_Type("populatedPlace", "Town"),
    "tramway": Local_Type("transportNetwork", "Tramway"),
    "urban_greenspace": Local_Type("landcover", "Urban_Greenspace"),
    "valley": Local_Type("landform", "Valley"),
    "vehicular_ferry_terminal": Local_Type("transportNetwork", "Vehicular_Ferry_Terminal"),
    "vehicular_rail_terminal": Local_Type("transportNetwork", "Vehicular_Rail_Terminal"),
    "village": Local_Type("populatedPlace", "Village"),
    "waterfall": Local_Type("hydrography", "Waterfall"),
    "wetland": Local_Type("landcover", "Wetland"),
    "woodland_or_forest": Local_Type("landcover", "Woodland_Or_Forest")
}


def validate_local_type(local_type: Union[str, Iterable]) -> set:
    local_type = {local_type} if isinstance(local_type, str) else set(local_type)
    return local_type - set(LOCAL_TYPE.keys())


def get_local_type(local_type_name: str) -> str:
    return LOCAL_TYPE[local_type_name].local_type
