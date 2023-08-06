import logging
import requests

from gracedb_sdk import Client

GRACEDB_BASE_URL = 'https://gracedb.ligo.org'
GRACEDB_EVENT_URL = f'{GRACEDB_BASE_URL}/superevents'
GRACEDB_API_URL = f'{GRACEDB_BASE_URL}/api/superevents/files'
SKIP_BASE_URL = 'http://skip.dev.hop.scimma.org'
SKIP_API_URL = f'{SKIP_BASE_URL}/api/events'

logger = logging.getLogger(__name__)


class GravitationalWaveClient:

    def __init__(self):
        self.gracedb_client = Client()

    def _get_fwhm_url(self, superevent_id):
        fwhm_data = {}

        try:
            fwhm_url = self.gracedb_client.superevents[superevent_id].files.get()['bayestar.volume.png']
            fwhm_data['fwhm_url'] = fwhm_url
        except Exception as e:
            logger.warn(f'Unable to retrieve FWHM URL for {superevent_id}: {e}')

        return fwhm_data

    def _get_skymap_url(self, superevent_id):
        skymap_data = {}

        try:
            skymap_url = self.gracedb_client.superevents[superevent_id].files.get()['bayestar.png']
            skymap_data['skymap_url'] = skymap_url
        except Exception as e:
            logger.warn(f'Unable to retrieve Skymap URL for {superevent_id}: {e}')

        return skymap_data

    def get_superevent_data(self, superevent_id: str) -> dict:
        url = requests.get(f'{SKIP_API_URL}/?identifier={superevent_id}').json()['results'][0]['event_detail']
        response = requests.get(url).json()
        superevent_data = {}
        superevent_data['event_data'] = response['event_attributes'][0]
        superevent_data['alerts'] = response['alerts']
        superevent_data['url'] = f'{GRACEDB_EVENT_URL}/{superevent_id}/'
        return superevent_data

    def get_additional_context_data(self, superevent_id: str) -> dict:
        additional_context_data = {}
        additional_context_data.update(self._get_fwhm_url(superevent_id))
        additional_context_data.update(self._get_skymap_url(superevent_id))
        return additional_context_data
