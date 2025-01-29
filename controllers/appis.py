import requests
import xml.etree.ElementTree as ET

def clima():
    url = 'http://api.weatherapi.com/v1/forecast.xml'
    params = {
        "key": "0d60aaaaa7fd4baf99c93801240111",
        "q": "El Salvador",
        "days": "1",
        "aqi": "no",
        "alerts": "no"
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        # Procesar el XML
        root = ET.fromstring(response.content)
        current = root.find('current')
        forecast = root.find('forecast').find('forecastday')
        
        datos = {
            "current": {
                "temperature": current.find('temp_c').text,
                "condition": current.find('condition').find('text').text,
                "wind_speed": current.find('wind_kph').text,
                "humidity": current.find('humidity').text,
            },
            "forecast": {
                "day": forecast.find('date').text,
                "temperature_min": forecast.find('day').find('mintemp_c').text,
                "temperature_max": forecast.find('day').find('maxtemp_c').text,
                "condition": forecast.find('day').find('condition').find('text').text,
            }
        }
        
        return datos
    
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    except ET.ParseError as parse_err:
        print(f"XML parse error: {parse_err}")
    
    return None

def get_Clima():
    API_KEY = 'q8xlcv52esndd5jbh3h3dan6kjhisvmocnq1swus'
    BASE_URL = 'https://www.meteosource.com/api/v1/free/point'
    
    params = {
        'place_id': 'El Salvador',
        'sections': 'current,hourly',
        'timezone': 'CST',
        'language': 'en',
        'units': 'auto',
        'key': API_KEY
    }
    
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 400:
        return response.json()
    else:
        print(f"Error al consulta los climas de la appi 2", response.status_code)
        return None