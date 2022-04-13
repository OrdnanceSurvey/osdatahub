from collections import namedtuple


Product = namedtuple("Product", "name geometry")


PREMIUM = {
    "topographic_area": Product("Topography_TopographicArea", "Polygon"),
    "topographic_point": Product("Topography_TopographicPoint", "Point"),
    "topographic_line": Product("Topography_TopographicLine", "LineString"),
    "water_network_link": Product("WaterNetwork_WatercourseLink", "LineString"),
    "water_network_node": Product("WaterNetwork_HydroNode", "Point"),
    "path_network_link": Product("DetailedPathNetwork_RouteLink", "LineString"),
    "path_network_node": Product("DetailedPathNetwork_RouteNode", "Point"),
    "highways_connecting_link": Product("Highways_ConnectingLink", "LineString"),
    "highways_connecting_node": Product("Highways_ConnectingNode", "Point"),
    "highways_ferry_link": Product("Highways_FerryLink", "LineString"),
    "highways_ferry_node": Product("Highways_FerryNode", "Point"),
    "highways_path_link": Product("Highways_PathLink", "LineString"),
    "highways_path_node": Product("Highways_PathNode", "Point"),
    "highways_road_link": Product("Highways_RoadLink", "LineString"),
    "highways_road_node": Product("Highways_RoadNode", "Point"),
    "highways_street": Product("Highways_Street", "LineString"),
    "greenspace_area": Product("Greenspace_GreenspaceArea", "Polygon"),
    "sites_access_point": Product("Sites_AccessPoint", "Point"),
    "sites_functional_site": Product("Sites_FunctionalSite", "Polygon"),
    "sites_routing_point": Product("Sites_RoutingPoint", "Point"),
    "topographic_boundary": Product("Topography_BoundaryLine", "LineString"),
    "cartographic_symbol": Product("Topography_CartographicSymbol", "Point"),
    "cartographic_text": Product("Topography_CartographicText", "Point"),
}


OPEN = {
    "zoomstack_district_buildings": Product("Zoomstack_DistrictBuildings", "Polygon"),
    "zoomstack_foreshore": Product("Zoomstack_Foreshore", "Polygon"),
    "zoomstack_greenspace": Product("Zoomstack_Greenspace", "Polygon"),
    "zoomstack_local_buildings": Product("Zoomstack_LocalBuildings", "Polygon"),
    "zoomstack_national_parks": Product("Zoomstack_NationalParks", "Polygon"),
    "zoomstack_sites": Product("Zoomstack_Sites", "Polygon"),
    "zoomstack_surface_water": Product("Zoomstack_Surfacewater", "Polygon"),
    "zoomstack_urban_areas": Product("Zoomstack_UrbanAreas", "Polygon"),
    "zoomstack_woodland": Product("Zoomstack_Woodland", "Polygon"),
    "zoomstack_boundaries": Product("Zoomstack_Boundaries", "LineString"),
    "zoomstack_contours": Product("Zoomstack_Contours", "LineString"),
    "zoomstack_ETL": Product("Zoomstack_ETL", "LineString"),
    "zoomstack_rail": Product("Zoomstack_Rail", "LineString"),
    "zoomstack_roads_local": Product("Zoomstack_RoadsLocal", "LineString"),
    "zoomstack_roads_national": Product("Zoomstack_RoadsNational", "LineString"),
    "zoomstack_roads_regional": Product("Zoomstack_RoadsRegional", "LineString"),
    "zoomstack_waterlines": Product("Zoomstack_Waterlines", "LineString"),
    "open_USRN": Product("OpenUSRN_USRN", "LineString"),
    "zoomstack_airports": Product("Zoomstack_Airports", "Point"),
    "zoomstack_names": Product("Zoomstack_Names", "Point"),
    "zoomstack_railway_stations": Product("Zoomstack_RailwayStations", "Point"),
    "openUPRN_address": Product("OpenUPRN_Address", "Point"),
    "openTOID_highways_network": Product("OpenTOID_HighwaysNetwork", "Point"),
    "openTOID_sites": Product("OpenTOID_SitesLayer", "Point"),
    "openTOID_topography": Product("OpenTOID_TopographyLayer", "Point"),
}


def suggest_product(text: str) -> list:
    matches = []
    for product_name in OPEN:
        if text in product_name:
            matches.append(f"{product_name} [OPEN]")
    for product_name in PREMIUM:
        if text in product_name:
            matches.append(f"{product_name} [PREMIUM]")
    return matches


def validate_product_name(product_name: str) -> str:
    if product_name in OPEN or product_name in PREMIUM:
        return product_name
    suggested_products = suggest_product(product_name)
    suggestion_str = (
        ", ".join(suggested_products)
        if len(suggested_products) > 0
        else "Can't find a match..."
    )
    raise ValueError(
        f"Unrecognised product '{product_name}'.\n\n"
        f"\tBest Matches: {suggestion_str}\n\n"
        f"\tOpen Products: {', '.join(list(OPEN))}\n\n"
        f"\tPremium Products: {', '.join(list(PREMIUM))}\n\n"
    )


def get_product(product_name: str):
    if product_name in PREMIUM:
        return PREMIUM[product_name]
    elif product_name in OPEN:
        return OPEN[product_name]
    else:
        raise ValueError(f"{product_name} is not a valid product name")
