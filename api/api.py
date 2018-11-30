import requests 
from requests.exceptions import ConnectionError

from exceptions import YandexException


class YandexRasp:
    version = 'v3.0'
    base_url = 'https://api.rasp.yandex.net'

    def __init__(self, api_key=None, domain=None):
        if api_key is None:
            raise YandexException('API KEY is required')
        self.api_key = api_key
        if domain is None:
            raise YandexException('Domain is required')
        self.domain = domain  
        self._client = requests.Session()

        self._client.headers.update({
            'Referer': self.domain, 
            'Authorization': self.api_key
        })

    def _make_request(self, endpoint, params):

        url = f'{self.base_url}/{self.version}/{endpoint}/'

        # self._client.headers.update({
        #     'Referer': self.domain, 
        #     'Authorization': self.api_key
        # })

        try:
            response = self._client.get(url, params=params)
            if response.status_code != 200:
                raise YandexException(response.json())
            return response.json()
        except ConnectionError:
            raise YandexException('Api not available')


    def search(self, from_, to, date, transport_types,coding_system,                       result_timezone,show_systems='yandex', format='json',                       lang='ru', offset=0, limit=100, add_days_mask=False,                        transfers=False):
        """ Get transport schedules between two stations
            https://api.rasp.yandex.net/v3.0/search/ ?
            from=<код станции отправления>
            & to=<код станции прибытия>
            & [format=<формат — XML или JSON>]
            & [lang=<язык>]
            & [apikey=<ключ>]
            & [date=<дата>]
            & [transport_types=<тип транспорта>]
            & [system=<система кодирования параметров to и from>]
            & [show_systems=<система кодирования для ответа>]
            & [offset=<сдвиг относительно первого рейса в ответе>]
            & [limit=<ограничение на количество рейсов в ответе>]
            & [add_days_mask=<запрос календаря хождения рейсов>]
            & [result_timezone=<часовой пояс>]
            & [transfers=<признак запроса маршрутов с пересадками>]
         """
        payload = {
             'from': from_,
             'to': to, 
             'lang': lang,
             'date': date, 
             'transport_types': transport_types,
             'system': coding_system,
             'offset': offset,
             'limit': limit,
             'add_days_mask': add_days_mask,
             'result_timezone': result_timezone,
             'transfers': transfers
         }

        return self._make_request('search', payload)

    def station_schedules(self, station, date, transport_types, event,                                  result_timezone, coding_system,                                             direction='departure',show_systems='yandex',                                lang='ru', format='json'):
        """ Get transport schedules for a particular station """

        payload = {
            'station': station,
            'direction': direction,
            'event': event,
             'lang': lang,
             'date': date, 
             'transport_types': transport_types,
             'system': coding_system,
             'result_timezone': result_timezone,
         }
        
        return self._make_request('schedule', payload)

    def thread_path(self, uid, from_, to, date, show_systems='yandex',                              lang='ru', format='json'):
        
        payload = {
            'uid': uid,
            'from': from_,
            'to': to, 
            'date': date,
            'show_systems': show_systems,
            'lang': lang,
            'format': format
        }

        return self._make_request('thread', payload)

    def nearest_stations(self, lat, lng, distance, transport_types,station_types, lang='ru', offset=0, limit=50, format='json'):
        
        endpoint = 'nearest_stations'

    def nearest_settlement(self, lat, lng, distance, lang='ru', format='json'):
        endpoint = 'nearest_settlement'

    def carrier(self, code, coding_system, lang='ru', format='json'):
        endpoint = 'carrier'

    def all_stations_list(self, lang='ru', format='json'):
        endpoint = 'stations_list'

    def copyright(self, format='json'):
        endpoint = 'copyright'

