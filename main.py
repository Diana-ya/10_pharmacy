import sys
from Samples.business import find_businesses
from Samples.distance import lonlat_distance
from Samples.geocoder import get_coordinates, get_ll_span
from Samples.mapapi_PG import show_map


def get_pharmacy_color(pharmacy):
    hours = pharmacy["properties"]["CompanyMetaData"].get("Hours", {})
    if not hours:
        return "pm2grm"
    if "круглосуточно" in hours.get("text", "").lower():
        return "pm2gnm"
    return "pm2blm"


def main():
    address = " ".join(sys.argv[1:])
    lon, lat = get_coordinates(address)

    address_ll = f"{lon},{lat}"
    span = "0.03,0.03"

    pharmacies = find_businesses(address_ll, span, "аптека")
    pharmacies.sort(key=lambda x: lonlat_distance((lon, lat),
                                                  (x["geometry"]["coordinates"][0], x["geometry"]["coordinates"][1])))
    pharmacies = pharmacies[:10]
    points_params = []
    points_params.append(f"{lon},{lat},pm2rdl")
    for pharmacy in pharmacies:
        point = pharmacy["geometry"]["coordinates"]
        color = get_pharmacy_color(pharmacy)
        points_params.append(f"{point[0]},{point[1]},{color}")

    points_str = "~".join(points_params)
    show_map(f"ll={address_ll}&spn={span}", "map", add_params=f"pt={points_str}")


if __name__ == "__main__":
    main()
