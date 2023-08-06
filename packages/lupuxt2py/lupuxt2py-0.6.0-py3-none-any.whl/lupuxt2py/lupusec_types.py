from dataclasses import dataclass
from enum import Enum
from typing import Tuple


class DeviceClass(Enum):
    ALARM_STATE = "alarm_state"
    KEYPAD = "keypad"
    SIREN = "siren"
    SWITCH = "switch"
    UNKNOWN = "unkown"
    CONTACT = "contact",
    MOTION = "motion",
    SMOKE = "smoke",


class AlarmMode(Enum):
    DISARM = 0,
    ARM_AWAY = 1,
    ARM_NIGHT = 2,
    ARM_HOME = 3


@dataclass()
class SystemInfo:

    def __init__(self, version: str = "", rf_ver: str = "", zb_ver: str = "", zbs_ver: str = "", gsm_ver: str = "", publicip: str = "", ip: str = "",
                 mac: str = ""):
        self.zbs_ver = zbs_ver
        self.gsm_ver = gsm_ver
        self.publicip = publicip
        self.ip = ip
        self.mac = mac
        self.zb_ver = zb_ver
        self.rf_ver = rf_ver
        self.version = version

    @property
    def unique_id(self):
        return self.mac.replace(":","")

@dataclass()
class AlarmPanel:
    mode: AlarmMode
    arm: int

    def __init__(self, mode: AlarmMode = AlarmMode.DISARM, f_arm: int = -1):
        self.mode = mode
        self.arm = f_arm


@dataclass()
class AlarmForm:
    __pcondform1: AlarmPanel
    __pcondform2: AlarmPanel

    def __init__(self, pcondform1: dict = {}, pcondform2: dict = {}):
        self.__pcondform1 = AlarmPanel(**pcondform1)
        self.__pcondform2 = AlarmPanel(**pcondform2)

    @property
    def area1_mode(self):
        return self.__pcondform1.mode

    @property
    def area1_arm(self):
        return bool(self.__pcondform1.arm)

    @property
    def area2_mode(self):
        return self.__pcondform2.mode

    @property
    def area2_arm(self):
        return bool(self.__pcondform2.arm)


@dataclass()
class Battery():
    """
    Daten-Container, welcher den Zustand der Batterie widerspiegelt
    """

    __battery: str
    __battery_ok: int

    def __init__(self, battery: str = "", battery_ok: int = -1, **kwargs):
        self.__battery = battery
        self.__battery_ok = battery_ok

    @property
    def is_ok(self) -> bool:
        return bool(self.__battery_ok)


@dataclass()
class Bypass():
    """
    Daten-Container, welcher den Zustand der zu ignorierende Sensormeldungen widerspiegelt
    """
    __bypass: int
    __bypass_tamper: int

    def __init__(self, bypass: int = -1, bypass_tamper: int = -1, **kwargs):
        self.__bypass = bypass
        self.__bypass_tamper = bypass_tamper
    @property
    def is_bypass_tamper(self) -> bool:
        return bool(self.__bypass_tamper)
    @property
    def is_bypass(self) -> bool:
        return bool(self.__bypass)
@dataclass()
class Tamper():
    """
    Daten-Container, welcher den Zustand des Sabotageschutzes eines Aktors widerspiegelt
    """
    __tamper: str
    __tamper_ok: int

    def __init__(self, tamper: str = "", tamper_ok: int = -1, **kwargs):
        self.__tamper = tamper
        self.__tamper_ok = tamper_ok
    @property
    def is_ok(self) -> bool:
        return bool(self.__tamper_ok)

@dataclass()
class Location():
    """
    Daten-Container, welcher den Standort des Aktors widerspiegelt
    """
    __zone: int
    __area: int

    def __init__(self, area: int = -1, zone: int = -1, **kwargs):
        self.__zone = zone
        self.__area = area
    @property
    def area_zone(self) -> Tuple[int,int]:
        return self.__zone,self.__area
@dataclass()
class LupuDevice():
    _type: int
    _sid: str
    _name: str
    _battery: Battery
    _tamper: Tamper
    _location: Location
    _bypass: Bypass
    _alarm_status: str
    _rssi: int

    def __init__(self, type: int = -1, sid: str = "", name: str = "", alarm_status: str = "", rssi: int = -1, **kwargs):
        self._rssi = rssi
        self._type = type
        self._sid = sid
        self._name = name
        self._alarm_status = alarm_status
        self._battery = Battery(**kwargs)
        self._tamper = Tamper(**kwargs)
        self._location = Location(**kwargs)
        self._bypass = Bypass(**kwargs)

    @property
    def sid(self):
        return self._sid

    @property
    def is_alarm(self):
        return  "BURGLAR" in self._alarm_status

    @property
    def battery(self) -> Battery:
        return self._battery

    @property
    def tamper(self) -> Tamper:
        return self._tamper

    @property
    def location(self) -> Location:
        return self._location

    @property
    def bypass(self) -> Bypass:
        return self._bypass

    @property
    def signal_strength(self) -> int:
        return self._rssi


# noinspection PyPep8Naming
@dataclass()
class ContactActor(LupuDevice):
    __open_close: int

    def __init__(self, openClose: int = -1, **kwargs):
        super().__init__(**kwargs)
        self.__open_close = openClose

    @property
    def is_open(self):
        return bool(self.__open_close)
# noinspection PyPep8Naming
@dataclass()
class SwitchActor(LupuDevice):
    __on_off: int

    def __init__(self, onOff: int = -1, **kwargs):
        super().__init__(**kwargs)
        self.__on_off = onOff

    @property
    def is_on(self):
        return bool(self.__on_off)


# noinspection PyPep8Naming
@dataclass()
class MotionActor(LupuDevice):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def is_moving(self):
        return "DOORBELL" in self._alarm_status
@dataclass()
class SmokeActor(LupuDevice):
    __is_moving: bool

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    @property
    def is_alarm(self):
        return "SMOKE" in self._alarm_status
