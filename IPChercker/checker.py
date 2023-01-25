import requests
import folium
import json


def get_info_by_ip(ip='127.0.0.1'):
    try:
        response = requests.get(url=f'http://ip-api.com/json/{ip}').json()

        data = {
            '[IP]': response.get('query'),
            '[Провайдер]': response.get('isp'),
            '[Організація]': response.get('org'),
            '[Країна]': response.get('country'),
            '[Назва регіону]': response.get('regionName'),
            '[Місто]': response.get('city'),
            '[Поштовий код]': response.get('zip'),
            '[Ширина]': response.get('lat'),
            '[Довгота]': response.get('lon')
        }

        '''for k, v in data.items():
            print(f'{k} : {v}')'''

        '''location_map = geocoder.ip(ip)
        address = location_map.latlng'''

        area = folium.Map(location=[response.get('lat'), response.get('lon')], zoom_start=12)
        folium.CircleMarker(location=[response.get('lat'), response.get('lon')],
                            popup="Yorkshire").add_to(area)
        area.save(f'Checked IP/checked_ip_map.html')

        with open(f'Checked IP/checked_ip_file.json', 'w') as currency_file:
            json.dump(data, currency_file, indent=4, ensure_ascii=False)

    except requests.exceptions.ConnectionError:
        print('[!] Будь ласка, перевірте правильність введених данних!')


def main():
    get_info_by_ip(ip='77.47.221.6')


if __name__ == '__main__':
    main()
    