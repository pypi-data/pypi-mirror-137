import base64
import json
import logging
from typing import Any, List, Dict

from urllib3 import HTTPResponse, PoolManager, Retry

from lupuxt2py.constants import *
from lupuxt2py.lupusec_types import *

_LOGGER = logging.getLogger("LupusecSevice")
logging.getLogger("urllib3").setLevel(logging.WARNING)


def _try_create(obj, func) -> LupuDevice:
    result = None
    try:
        result = func(obj)
    except Exception as ex:
        _LOGGER.error(ex)
    return result


def _normalize(data):
    text = data.decode('utf-8')
    text = text.replace("\n", "").replace("\t", "").replace("\r", "").replace("\0", "")
    text = text.replace("{WEB_MSG_STRONG}", "").replace("{WEB_MSG_WEAK}", "").replace("{WEB_MSG_NA}", "0").replace("{WEB_MSG_GOOD}", "")
    return text


class LupusecSevice:
    """Interface to Lupusec Webservices."""

    def __init__(self, username, password, ip_address):
        """LupsecAPI constructor requires IP and credentials to the
        Lupusec Webinterface.
        """
        self.api_url = "http://{}".format(ip_address)
        creds = f"{username}:{password}".encode("latin1")
        auth = "Basic %s" % base64.b64encode(creds).decode("latin1")
        self.__headers = {"Authorization": auth}
        self.__http = PoolManager(num_pools=10, headers=self.__headers, retries=Retry(2))
        token = self.__get_token()
        self.__http.headers.setdefault("X-Token", token)
        """action/deviceListGet"""

    async def get_sensor_list_async(self):
        return self.get_sensor_list()

    def get_sensor_list(self) -> Dict[DeviceClass, List[LupuDevice]]:
        data = self.__get_request(urlDeviceGet, {})
        _LOGGER.debug("Antwort von Lupusec %s:\n%s", urlDeviceGet, json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2))
        lst = list(
            filter(lambda x: "type" in x.keys() and not int(x["type"]) == 81 and (not "always_off" in x.keys() or int(x["always_off"]) == 0), data["senrows"]))
        contacts = self.__map_to_actor(lst, lambda x: _try_create(x, lambda it: ContactActor(**it)), lambda x: "openClose" in x.keys())
        switches = self.__map_to_actor(lst, lambda x: _try_create(x, lambda it: SwitchActor(**it)), lambda x: "onOff" in x.keys())
        motions = self.__map_to_actor(lst, lambda x: _try_create(x, lambda it: MotionActor(**it)), lambda x: int(x["type"]) == 9)
        keypads = self.__map_to_actor(lst, lambda x: _try_create(x, lambda it: LupuDevice(**it)), lambda x: int(x["type"]) == 37)
        sirens = self.__map_to_actor(lst, lambda x: _try_create(x, lambda it: LupuDevice(**it)),
                                     lambda x: [45, 46, 22].__contains__(int(x["type"])) and not "manu" in x.keys())
        smokes = self.__map_to_actor(lst, lambda x: _try_create(x, lambda it: LupuDevice(**it)), lambda x: int(x["type"]) == 11)
        alarm_state_views = self.__map_to_actor(lst, lambda x: _try_create(x, lambda it: LupuDevice(**it)),
                                                lambda x: int(x["type"]) == 22 and "manu" in x.keys())
        devices = {DeviceClass.CONTACT: contacts, DeviceClass.SWITCH: switches, DeviceClass.MOTION: motions, DeviceClass.SMOKE: smokes,
                   DeviceClass.SIREN: sirens, DeviceClass.KEYPAD: keypads, DeviceClass.ALARM_STATE: alarm_state_views}
        flatten = [val for sublist in devices.values() for val in sublist]
        for item in lst:
            found = list(filter(lambda x: x.sid == item["sid"], flatten)).__len__() > 0
            if not found:
                _LOGGER.info(item["name"] + " nicht gefunden")
        _LOGGER.debug(flatten)
        return devices

    async def get_alarm_panel_async(self):
        return self.get_alarm_panel()

    def get_alarm_panel(self) -> AlarmForm:
        data = self.__get_request(urlPanelCondGet, {})
        _LOGGER.debug("Antwort von Lupusec %s:\n%s", urlDeviceGet, json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2))
        form = AlarmForm(**data["forms"])
        _LOGGER.debug(form)
        return form

    def __map_to_actor(self, lst, actorFactory, predicate):
        openerContacts = filter(predicate, lst)
        return [actorFactory(contacts) for contacts in openerContacts]

    async def post_activate_alarm_mode_async(self, area: int, alarm_mode: AlarmMode) -> None:
        self.post_activate_alarm_mode(area,alarm_mode)



    def post_activate_alarm_mode(self, area: int, alarm_mode: AlarmMode) -> None:
        self.__post_request('/action/panelCondPost',
                            {"area": str(area), "mode": str(alarm_mode.value)}
                            )

    def post_switch_device_async(self, id: str, onOff: bool) -> None:
        self.post_switch_device(id,onOff)

    def post_switch_device(self, id: str, onOff: bool) -> None:
        encodedFormParams = {"switch": str(onOff.__int__()),
                             "pd": "",
                             "id": id}
        self.__post_request('/action/deviceSwitchPSSPost', encodedFormParams)

    def __get_request(self, apiPart: str, data: Any = None) -> HTTPResponse:
        response: HTTPResponse = self.__http.request('GET', self.api_url + apiPart, fields=data)
        data = _normalize(response.data)
        return json.loads(data)

    def __post_request(self, apiPart: str, data: Any) -> HTTPResponse:
        response = self.__http.request('POST', self.api_url + apiPart, fields=data)
        return response

    def __get_token(self) -> str:
        data = self.__get_request(urlTokenGet)
        return data["message"]
