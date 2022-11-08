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

    "Topography_TopographicArea": Product("Topography_TopographicArea", "Polygon"),
    "Topography_TopographicPoint": Product("Topography_TopographicPoint", "Point"),
    "Topography_TopographicLine": Product("Topography_TopographicLine", "LineString"),
    "WaterNetwork_WatercourseLink": Product("WaterNetwork_WatercourseLink", "LineString"),
    "WaterNetwork_HydroNode": Product("WaterNetwork_HydroNode", "Point"),
    "DetailedPathNetwork_RouteLink": Product("DetailedPathNetwork_RouteLink", "LineString"),
    "DetailedPathNetwork_RouteNode": Product("DetailedPathNetwork_RouteNode", "Point"),
    "Highways_ConnectingLink": Product("Highways_ConnectingLink", "LineString"),
    "Highways_ConnectingNode": Product("Highways_ConnectingNode", "Point"),
    "Highways_FerryLink": Product("Highways_FerryLink", "LineString"),
    "Highways_FerryNode": Product("Highways_FerryNode", "Point"),
    "Highways_PathLink": Product("Highways_PathLink", "LineString"),
    "Highways_PathNode": Product("Highways_PathNode", "Point"),
    "Highways_RoadLink": Product("Highways_RoadLink", "LineString"),
    "Highways_RoadNode": Product("Highways_RoadNode", "Point"),
    "Highways_Street": Product("Highways_Street", "LineString"),
    "Greenspace_GreenspaceArea": Product("Greenspace_GreenspaceArea", "Polygon"),
    "Sites_AccessPoint": Product("Sites_AccessPoint", "Point"),
    "Sites_FunctionalSite": Product("Sites_FunctionalSite", "Polygon"),
    "Sites_RoutingPoint": Product("Sites_RoutingPoint", "Point"),
    "Topography_BoundaryLine": Product("Topography_BoundaryLine", "LineString"),
    "Topography_CartographicSymbol": Product("Topography_CartographicSymbol", "Point"),
    "Topography_CartographicText": Product("Topography_CartographicText", "Point")
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
    "Zoomstack_DistrictBuildings": Product("Zoomstack_DistrictBuildings", "Polygon"),
    "Zoomstack_Foreshore": Product("Zoomstack_Foreshore", "Polygon"),
    "Zoomstack_Greenspace": Product("Zoomstack_Greenspace", "Polygon"),
    "Zoomstack_LocalBuildings": Product("Zoomstack_LocalBuildings", "Polygon"),
    "Zoomstack_NationalParks": Product("Zoomstack_NationalParks", "Polygon"),
    "Zoomstack_Sites": Product("Zoomstack_Sites", "Polygon"),
    "Zoomstack_Surfacewater": Product("Zoomstack_Surfacewater", "Polygon"),
    "Zoomstack_UrbanAreas": Product("Zoomstack_UrbanAreas", "Polygon"),
    "Zoomstack_Woodland": Product("Zoomstack_Woodland", "Polygon"),
    "Zoomstack_Boundaries": Product("Zoomstack_Boundaries", "LineString"),
    "Zoomstack_Contours": Product("Zoomstack_Contours", "LineString"),
    "Zoomstack_ETL": Product("Zoomstack_ETL", "LineString"),
    "Zoomstack_Rail": Product("Zoomstack_Rail", "LineString"),
    "Zoomstack_RoadsLocal": Product("Zoomstack_RoadsLocal", "LineString"),
    "Zoomstack_RoadsNational": Product("Zoomstack_RoadsNational", "LineString"),
    "Zoomstack_RoadsRegional": Product("Zoomstack_RoadsRegional", "LineString"),
    "Zoomstack_Waterlines": Product("Zoomstack_Waterlines", "LineString"),
    "OpenUSRN_USRN": Product("OpenUSRN_USRN", "LineString"),
    "Zoomstack_Airports": Product("Zoomstack_Airports", "Point"),
    "Zoomstack_Names": Product("Zoomstack_Names", "Point"),
    "Zoomstack_RailwayStations": Product("Zoomstack_RailwayStations", "Point"),
    "openUPRN_address": Product("OpenUPRN_Address", "Point"),
    "OpenTOID_HighwaysNetwork": Product("OpenTOID_HighwaysNetwork", "Point"),
    "OpenTOID_SitesLayer": Product("OpenTOID_SitesLayer", "Point"),
    "OpenTOID_TopographyLayer": Product("OpenTOID_TopographyLayer", "Point")
}


def convert_product_to_new_geometry(product: Product) -> Product:
    """
    Takes a Product object and returns a copy with an updated geometry for the new API endpoint.
    The new API returns a MultiPolygon and a MultiLineString where the old API returned a Polygon and Linestring
    respectively.
    Args:
        product Product): Product object to convert

    Returns (Product): a copy of the Product object with updated geometry.
    """
    if product.geometry == "LineString":
        new_geom = "MultiLineString"
    elif product.geometry == "Polygon":
        new_geom = "MultiPolygon"
    elif product.geometry in ("Point", "MultiPolygon", "MultiLineString"):
        new_geom = product.geometry
    else:
        raise ValueError(f"argument product has an invalid geometry. Must be one of Point, Polygon, LineString, "
                         f"MultiPolygon, MultiLineString, but was {product.geometry}")

    return Product(product.name, new_geom)


OPEN_NEW = {key: convert_product_to_new_geometry(value) for key, value in OPEN.items()}

PREMIUM_NEW = {key: convert_product_to_new_geometry(value) for key, value in PREMIUM.items()}


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
    suggestion_str = ", ".join(suggested_products) \
        if len(suggested_products) > 0 else "Can't find a match..."
    raise ValueError(f"Unrecognised product '{product_name}'.\n\n" \
                     f"\tBest Matches: {suggestion_str}\n\n" \
                     f"\tOpen Products: {', '.join(list(OPEN))}\n\n" \
                     f"\tPremium Products: {', '.join(list(PREMIUM))}\n\n")


def get_product(product_name: str, new_api: bool = False) -> Product:
    premium_lookup = PREMIUM_NEW if new_api else PREMIUM
    open_lookup = OPEN_NEW if new_api else OPEN
    if product_name in premium_lookup:
        return premium_lookup[product_name]
    elif product_name in open_lookup:
        return open_lookup[product_name]
    else:
        raise ValueError(f"{product_name} is not a valid product name")