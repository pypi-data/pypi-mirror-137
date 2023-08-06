import asyncio
import logging

from lupuxt2py.lupusec_service import LupusecSevice


_LOGGER = logging.getLogger("LupusecStateMachine")


class LupusecStateMachine:

    def __init__(self, username, password, ip_address, time):
        self.__time = time
        self.__devicesDict = dict()
        self.__panels = None
        self.__lupu_service = LupusecSevice(username, password, ip_address)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.__poll_devices())
        loop.run_until_complete(self.__poll_panels())

    def __refresh_devices(self):
        try:
            self.__devicesDict = self.__lupu_service.get_sensor_list()
        except Exception as ex:
            _LOGGER.error(ex)

    def __refresh_panels(self):
        try:
            self.__panels = self.__lupu_service.get_alarm_panel()
        except Exception as ex:
            _LOGGER.error(ex)

    async def __poll_devices(self):
        while True:
            await asyncio.sleep(self.__time)
            self.__refresh_devices()

    async def __poll_panels(self):
        while True:
            await asyncio.sleep(self.__time)
            self.__refresh_panels()

    @property
    def devices(self):
        return self.__devicesDict

    @property
    def panels(self):
        return self.__panels
