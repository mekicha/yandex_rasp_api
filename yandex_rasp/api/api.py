import requests
from requests.exceptions import ConnectionError

from exceptions import YandexException


class YandexRasp:
    doc_page = "https://tech.yandex.ru/rasp/doc/concepts/access-docpage/"
    version = "v3.0"
    base_url = "https://api.rasp.yandex.net"

    def __init__(self, api_key=None, domain=None):
        if api_key is None:
            raise YandexException("API KEY is required")
        self.api_key = api_key
        if domain is None:
            msg = "Domain is required. See {} for why".format(self.doc_page)
            raise YandexException(msg)
        self.domain = domain
        self._client = requests.Session()

        self._client.headers.update(
            {"Referer": self.domain, "Authorization": self.api_key}
        )

    def _make_request(self, endpoint, params):

        url = f"{self.base_url}/{self.version}/{endpoint}/"

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
            raise YandexException("Api not available")

    def search(
        self,
        from_,
        to,
        date,
        transport_types,
        coding_system,
        result_timezone,
        show_systems="yandex",
        format="json",
        lang="ru",
        offset=0,
        limit=100,
        add_days_mask=False,
        transfers=False,
    ):
        """ Get transport schedules between two stations """
        payload = {
            "from": from_,
            "to": to,
            "lang": lang,
            "date": date,
            "transport_types": transport_types,
            "system": coding_system,
            "offset": offset,
            "limit": limit,
            "add_days_mask": add_days_mask,
            "result_timezone": result_timezone,
            "transfers": transfers,
        }

        return self._make_request("search", payload)

    def station_schedules(
        self,
        station,
        date,
        transport_types,
        event,
        result_timezone,
        coding_system,
        direction="departure",
        show_systems="yandex",
        lang="ru",
        format="json",
    ):
        """ Get transport schedules for a particular station """

        payload = {
            "station": station,
            "direction": direction,
            "event": event,
            "lang": lang,
            "date": date,
            "transport_types": transport_types,
            "system": coding_system,
            "result_timezone": result_timezone,
        }

        return self._make_request("schedule", payload)

    def thread_path(
        self, uid, from_, to, date, show_systems="yandex", lang="ru", format="json"
    ):
        """ Get a list of stations following a thread by
         the specified thread ID(uid)
        """

        endpoint = "thread"

        payload = {
            "uid": uid,
            "from": from_,
            "to": to,
            "date": date,
            "show_systems": show_systems,
            "lang": lang,
            "format": format,
        }

        return self._make_request(endpoint, payload)

    def nearest_stations(
        self,
        lat,
        lng,
        distance,
        transport_types,
        station_types,
        lang="ru",
        offset=0,
        limit=50,
        format="json",
    ):
        """ get the list of stations located in the specified 
            radius(distance) from the specified point(lat, lng)
        """

        endpoint = "nearest_stations"
        payload = {
            "lat": lat,
            "lng": lng,
            "distance": distance,
            "transport_types": transport_types,
            "station_types": station_types,
            "lang": lang,
            "offset": offset,
            "limit": limit,
            "format": format,
        }

        return self._make_request(endpoint, payload)

    def nearest_settlement(self, lat, lng, distance, lang="ru", format="json"):
        """ get information about the nearest town from
            specified point(lat, lng)
        """

        endpoint = "nearest_settlement"

        payload = {
            "lat": lat,
            "lng": lng,
            "distance": distance,
            "lang": lang,
            "format": format,
        }

        return self._make_request(endpoint, payload)

    def carrier(self, code, coding_system, lang="ru", format="json"):
        """ get information about the carrier using
            specified carrier code (code)
        """

        endpoint = "carrier"

        payload = {
            "code": code,
            "coding_system": coding_system,
            "lang": lang,
            "format": format,
        }

        return self._make_request(endpoint, payload)

    def all_stations_list(self, lang="ru", format="json"):
        """ Get all stations list """

        endpoint = "stations_list"

        payload = {"lang": lang, "format": format}

        return self._make_request(endpoint, payload)

    def copyright(self, format="json"):
        """ Get the about data of the Yandex Rasp service """

        endpoint = "copyright"

        return self._make_request(endpoint, {"format": format})
