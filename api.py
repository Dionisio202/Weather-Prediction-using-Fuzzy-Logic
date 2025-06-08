import requests
import pandas as pd
from datetime import datetime, timedelta
import time

# Configuración de las claves API de Weatherbit
api_keys = [
    "6a93c40ee84a4d10a94ba6329948d615",
    "76af19c38fec42dd98d9f4a0cec16603",
    "c534297ff52448bcab14116515f136e9",
    "17d33c97f8744d629ec593bba370c7e1"
]

# Lista de ubicaciones (todas las ciudades que deseas cubrir)
locations = [
    {"lat": "0.9592", "lon": "-79.6539", "name": "Esmeraldas, Ecuador"},
    {"lat": "-0.2535", "lon": "-79.1754", "name": "Santo Domingo, Ecuador"},
    {"lat": "-0.1807", "lon": "-78.4678", "name": "Quito, Ecuador"},
    {"lat": "-1.2491", "lon": "-78.6168", "name": "Ambato, Ecuador"},
    {"lat": "-1.4924", "lon": "-77.0519", "name": "Puyo, Ecuador"},
    {"lat": "-0.921", "lon": "-77.7329", "name": "Napo, Ecuador"},
    {"lat": "-2.8974", "lon": "-79.0045", "name": "Cuenca, Ecuador"},
    {"lat": "-4.0079", "lon": "-79.2113", "name": "Loja, Ecuador"},
    # Ciudades adicionales de diferentes partes del mundo
    {"lat": "40.7128", "lon": "-74.0060", "name": "New York, USA"},
    {"lat": "34.0522", "lon": "-118.2437", "name": "Los Angeles, USA"},
    {"lat": "41.8781", "lon": "-87.6298", "name": "Chicago, USA"},
    {"lat": "51.5074", "lon": "-0.1278", "name": "London, UK"},
    {"lat": "48.8566", "lon": "2.3522", "name": "Paris, France"},
    {"lat": "35.6895", "lon": "139.6917", "name": "Tokyo, Japan"},
    {"lat": "-33.8688", "lon": "151.2093", "name": "Sydney, Australia"},
    {"lat": "-23.5505", "lon": "-46.6333", "name": "São Paulo, Brazil"},
    {"lat": "55.7558", "lon": "37.6173", "name": "Moscow, Russia"},
    {"lat": "19.4326", "lon": "-99.1332", "name": "Mexico City, Mexico"},
    {"lat": "28.6139", "lon": "77.2090", "name": "New Delhi, India"},
    {"lat": "-34.6037", "lon": "-58.3816", "name": "Buenos Aires, Argentina"},
    {"lat": "31.2304", "lon": "121.4737", "name": "Shanghai, China"},
    {"lat": "1.3521", "lon": "103.8198", "name": "Singapore"},
    {"lat": "52.5200", "lon": "13.4050", "name": "Berlin, Germany"},
    {"lat": "37.7749", "lon": "-122.4194", "name": "San Francisco, USA"},
    {"lat": "43.6532", "lon": "-79.3832", "name": "Toronto, Canada"},
    {"lat": "45.4642", "lon": "9.1900", "name": "Milan, Italy"},
    {"lat": "22.3964", "lon": "114.1095", "name": "Hong Kong"},
    {"lat": "31.7683", "lon": "35.2137", "name": "Jerusalem, Israel"},
    {"lat": "39.9042", "lon": "116.4074", "name": "Beijing, China"},
    {"lat": "25.2048", "lon": "55.2708", "name": "Dubai, UAE"},
    {"lat": "41.3851", "lon": "2.1734", "name": "Barcelona, Spain"},
    {"lat": "-22.9068", "lon": "-43.1729", "name": "Rio de Janeiro, Brazil"},
    {"lat": "13.7563", "lon": "100.5018", "name": "Bangkok, Thailand"},
    {"lat": "37.5665", "lon": "126.9780", "name": "Seoul, South Korea"},
    {"lat": "-33.9249", "lon": "18.4241", "name": "Cape Town, South Africa"},
    {"lat": "50.1109", "lon": "8.6821", "name": "Frankfurt, Germany"},
    {"lat": "52.3676", "lon": "4.9041", "name": "Amsterdam, Netherlands"},
    {"lat": "41.9028", "lon": "12.4964", "name": "Rome, Italy"},
    {"lat": "30.0444", "lon": "31.2357", "name": "Cairo, Egypt"},
    {"lat": "14.5995", "lon": "120.9842", "name": "Manila, Philippines"},
    {"lat": "6.5244", "lon": "3.3792", "name": "Lagos, Nigeria"},
    {"lat": "-37.8136", "lon": "144.9631", "name": "Melbourne, Australia"},
    {"lat": "45.5017", "lon": "-73.5673", "name": "Montreal, Canada"},
    {"lat": "18.5204", "lon": "73.8567", "name": "Pune, India"},
    {"lat": "40.4168", "lon": "-3.7038", "name": "Madrid, Spain"},
    {"lat": "34.6937", "lon": "135.5023", "name": "Osaka, Japan"},
    {"lat": "50.0755", "lon": "14.4378", "name": "Prague, Czech Republic"},
    {"lat": "60.1699", "lon": "24.9384", "name": "Helsinki, Finland"},
    {"lat": "59.3293", "lon": "18.0686", "name": "Stockholm, Sweden"},
    {"lat": "53.3498", "lon": "-6.2603", "name": "Dublin, Ireland"},
    {"lat": "47.4979", "lon": "19.0402", "name": "Budapest, Hungary"},
    {"lat": "55.6761", "lon": "12.5683", "name": "Copenhagen, Denmark"},
    {"lat": "35.8617", "lon": "104.1954", "name": "China"},
    {"lat": "41.0082", "lon": "28.9784", "name": "Istanbul, Turkey"},
    {"lat": "3.1390", "lon": "101.6869", "name": "Kuala Lumpur, Malaysia"},
    {"lat": "-6.2088", "lon": "106.8456", "name": "Jakarta, Indonesia"},
    {"lat": "-1.2921", "lon": "36.8219", "name": "Nairobi, Kenya"},
    {"lat": "36.2048", "lon": "138.2529", "name": "Japan"},
    {"lat": "56.1304", "lon": "-106.3468", "name": "Canada"},
    {"lat": "-25.2744", "lon": "133.7751", "name": "Australia"},
    {"lat": "64.9631", "lon": "-19.0208", "name": "Iceland"},
    {"lat": "46.8182", "lon": "8.2275", "name": "Switzerland"},
    {"lat": "61.9241", "lon": "25.7482", "name": "Finland"},
    {"lat": "46.2276", "lon": "2.2137", "name": "France"},
    {"lat": "55.3781", "lon": "-3.4360", "name": "United Kingdom"},
    {"lat": "51.1657", "lon": "10.4515", "name": "Germany"},
    {"lat": "41.8719", "lon": "12.5674", "name": "Italy"},
    {"lat": "-15.7942", "lon": "-47.8822", "name": "Brasilia, Brazil"},
    {"lat": "4.7110", "lon": "-74.0721", "name": "Bogotá, Colombia"},
    {"lat": "-12.0464", "lon": "-77.0428", "name": "Lima, Peru"},
    {"lat": "10.4806", "lon": "-66.9036", "name": "Caracas, Venezuela"},
    {"lat": "18.4663", "lon": "-66.1057", "name": "San Juan, Puerto Rico"},
    {"lat": "18.1096", "lon": "-77.2975", "name": "Kingston, Jamaica"},
    {"lat": "0.3476", "lon": "32.5825", "name": "Kampala, Uganda"},
    {"lat": "9.0054", "lon": "38.7636", "name": "Addis Ababa, Ethiopia"},
    {"lat": "-1.9403", "lon": "29.8739", "name": "Kigali, Rwanda"},
    {"lat": "31.7917", "lon": "-7.0926", "name": "Morocco"},
    {"lat": "24.7136", "lon": "46.6753", "name": "Riyadh, Saudi Arabia"},
    {"lat": "35.6892", "lon": "51.3890", "name": "Tehran, Iran"},
    {"lat": "33.8938", "lon": "35.5018", "name": "Beirut, Lebanon"},
    {"lat": "31.9522", "lon": "35.2332", "name": "Amman, Jordan"},
    {"lat": "33.5138", "lon": "36.2765", "name": "Damascus, Syria"},
    {"lat": "-22.9707", "lon": "-43.1824", "name": "Rio de Janeiro, Brazil"},
    {"lat": "-34.9285", "lon": "138.6007", "name": "Adelaide, Australia"},
    {"lat": "-8.4095", "lon": "115.1889", "name": "Bali, Indonesia"},
    {"lat": "45.8150", "lon": "15.9819", "name": "Zagreb, Croatia"},
    {"lat": "55.9533", "lon": "-3.1883", "name": "Edinburgh, Scotland"},
    {"lat": "51.5074", "lon": "-0.1278", "name": "London, UK"},
    {"lat": "51.1657", "lon": "10.4515", "name": "Germany"},
    {"lat": "40.7128", "lon": "-74.0060", "name": "New York City, USA"},
    {"lat": "35.8617", "lon": "104.1954", "name": "China"},
    {"lat": "-33.8688", "lon": "151.2093", "name": "Sydney, Australia"},
    {"lat": "35.6895", "lon": "139.6917", "name": "Tokyo, Japan"},
    {"lat": "19.075984", "lon": "72.877656", "name": "Mumbai, India"},
    {"lat": "55.7558", "lon": "37.6173", "name": "Moscow, Russia"},
    {"lat": "48.8566", "lon": "2.3522", "name": "Paris, France"},
    {"lat": "41.0082", "lon": "28.9784", "name": "Istanbul, Turkey"},
    {"lat": "40.4168", "lon": "-3.7038", "name": "Madrid, Spain"},
    {"lat": "37.7749", "lon": "-122.4194", "name": "San Francisco, USA"},
    {"lat": "-34.6037", "lon": "-58.3816", "name": "Buenos Aires, Argentina"},
    {"lat": "-23.5505", "lon": "-46.6333", "name": "São Paulo, Brazil"}
    # Puedes agregar más ciudades si lo deseas
]

start_date = datetime(2021, 1, 1)
end_date = datetime(2023, 12, 31)
weather_data_list = []
max_days_per_request = 365  # Aumentado de 15 a 365
current_api_key_index = 0
requests_made = 0
max_requests_per_key = 1500  # Número máximo de solicitudes por clave API

for current_location in locations:
    current_start_date = start_date
    while current_start_date <= end_date:
        current_end_date = min(current_start_date + timedelta(days=max_days_per_request - 1), end_date)
        start_str = current_start_date.strftime('%Y-%m-%d')
        end_str = current_end_date.strftime('%Y-%m-%d')
        current_api_key = api_keys[current_api_key_index]

        url = f"https://api.weatherbit.io/v2.0/history/daily?lat={current_location['lat']}&lon={current_location['lon']}&start_date={start_str}&end_date={end_str}&key={current_api_key}"

        # Intentar la solicitud con reintentos en caso de error
        for attempt in range(3):  # Intentar hasta 3 veces
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 429:
                    # Código de estado 429 significa "Too Many Requests"
                    print(f"Límite de solicitudes alcanzado para la clave {current_api_key}. Cambiando a la siguiente clave.")
                    current_api_key_index += 1
                    if current_api_key_index >= len(api_keys):
                        print("No hay más claves API disponibles. Deteniendo el script.")
                        exit()
                    current_api_key = api_keys[current_api_key_index]
                    # Actualizar la URL con la nueva clave
                    url = f"https://api.weatherbit.io/v2.0/history/daily?lat={current_location['lat']}&lon={current_location['lon']}&start_date={start_str}&end_date={end_str}&key={current_api_key}"
                    # Reiniciar el contador de solicitudes
                    requests_made = 0
                    # Reintentar la solicitud con la nueva clave
                    continue
                response.raise_for_status()  # Genera un error si la respuesta no es 200
                data = response.json()

                for daily_data in data['data']:
                    daily_data['lat'] = float(current_location['lat'])
                    daily_data['lon'] = float(current_location['lon'])
                    daily_data['location'] = current_location['name']

                    for key, value in daily_data.items():
                        if isinstance(value, float) and value.is_integer():
                            daily_data[key] = int(value)

                    weather_data_list.append(daily_data)

                print(f"Datos desde {start_str} hasta {end_str} agregados exitosamente para {current_location['name']}.")
                requests_made += 1
                if requests_made >= max_requests_per_key:
                    print(f"Límite de solicitudes alcanzado para la clave {current_api_key}. Cambiando a la siguiente clave.")
                    current_api_key_index += 1
                    if current_api_key_index >= len(api_keys):
                        print("No hay más claves API disponibles. Deteniendo el script.")
                        exit()
                    current_api_key = api_keys[current_api_key_index]
                    requests_made = 0
                break  # Salir del ciclo si la solicitud fue exitosa

            except requests.exceptions.RequestException as e:
                print(f"Error en intento {attempt + 1} para {current_location['name']} desde {start_str} hasta {end_str}: {e}")
                time.sleep(5)  # Esperar antes de reintentar

        current_start_date = current_end_date + timedelta(days=1)

# Convertir los datos en un DataFrame y guardarlos
weather_data = pd.DataFrame(weather_data_list)
weather_data.to_csv("datos_weatherbit_diarios4.csv", index=False)
print("Datos guardados en 'datos_weatherbit_diarios4.csv'")