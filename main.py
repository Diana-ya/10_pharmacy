import sys
from Samples.business import find_businesses
from Samples.distance import lonlat_distance
from Samples.geocoder import get_coordinates, get_ll_span
from Samples.mapapi_PG import show_map


def get_pharmacy_color(pharmacy):
    hours = pharmacy["properties"]["CompanyMetaData"].get("Hours", {})
    if not hours:
        return "pm2grm"  # серый - нет данных
    if "круглосуточно" in hours.get("text", "").lower():
        return "pm2gnm"  # зеленый - круглосуточно
    return "pm2blm"  # синий - не круглосуточно


def main():
    if len(sys.argv) < 2:
        print("Укажите адрес в командной строке")
        return

    address = " ".join(sys.argv[1:])
    lon, lat = get_coordinates(address)
    if not lat or not lon:
        print("Адрес не найден")
        return

    address_ll = f"{lon},{lat}"
    span = "0.04,0.04"

    pharmacies = find_businesses(address_ll, span, "аптека")
    if not pharmacies:
        print("Аптеки не найдены")
        return

    pharmacies.sort(key=lambda x: lonlat_distance((lon, lat),
                                                  (x["geometry"]["coordinates"][0], x["geometry"]["coordinates"][1])))
    pharmacies = pharmacies[:10]

    points_params = []
    for pharmacy in pharmacies:
        point = pharmacy["geometry"]["coordinates"]
        color = get_pharmacy_color(pharmacy)
        points_params.append(f"{point[0]},{point[1]},{color}")

    points_params.append(f"{lon},{lat},pm2rdl")
    max_points_per_request = 10
    for i in range(0, len(points_params), max_points_per_request):
        points_str = "~".join(points_params[i:i + max_points_per_request])

        show_map(f"ll={address_ll}&spn={span}", "map", add_params=f"pt={points_str}")


if __name__ == "__main__":
    main()
