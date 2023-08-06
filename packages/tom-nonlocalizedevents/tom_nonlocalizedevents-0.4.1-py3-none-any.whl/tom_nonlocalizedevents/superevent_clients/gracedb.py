from urllib3.response import HTTPResponse

from gracedb_sdk import Client
import voeventparse as vp


GRACEDB_BASE_URL = 'https://gracedb.ligo.org'
GRACEDB_EVENT_URL = f'{GRACEDB_BASE_URL}/superevents'
GRACEDB_API_URL = f'{GRACEDB_BASE_URL}/api/superevents'


@DeprecationWarning
class GraceDBClient:

    def __init__(self, *args, **kwargs):
        self.gracedb_client = Client()

    def get_superevent_data(self, superevent_id: str) -> dict:
        print('this isn\'t great')
        try:
            gracedb_superevent = self.gracedb_client.superevents[superevent_id]
            gracedb_data = gracedb_superevent.get()
            latest_voevent = gracedb_superevent.voevents.get()[-1]
            voevent_file = gracedb_superevent.files[latest_voevent['filename']].get()

            superevent_data = {}
            superevent_data['update_version'] = latest_voevent['filename'].split('-')[1]
            superevent_data['far'] = gracedb_data['far']
            superevent_data['instruments'] = gracedb_data['preferred_event_data']['instruments']
            superevent_data.update(self.get_data_from_voevent(voevent_file))
            return superevent_data
        except Exception as e:
            print(f'exception {e}')
            return {}

    # TODO: error handle the crap out of this
    def get_data_from_voevent(self, voevent_file: HTTPResponse) -> dict:
        voevent = vp.load(voevent_file)
        voevent_data = {}

        classification_group = voevent.What.find(".//Group[@type='Classification']")
        for datum in ['BNS', 'NSBH', 'BBH', 'MassGap', 'Terrestrial']:
            datum_element = classification_group.find(f".//Param[@name='{datum}']")
            if datum_element is not None:
                voevent_data[datum] = datum_element.attrib['value']

        properties_group = voevent.What.find(".//Group[@type='Properties']")
        for datum in ['HasNS', 'HasRemnant']:
            datum_element = properties_group.find(f".//Param[@name='{datum}']")
            if datum_element is not None:
                voevent_data[datum] = datum_element.attrib['value']

        return voevent_data
