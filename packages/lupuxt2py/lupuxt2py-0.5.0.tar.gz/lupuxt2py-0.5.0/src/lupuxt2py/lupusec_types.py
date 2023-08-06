from dataclasses import dataclass
from enum import Enum


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
class AlarmPanel:
    __mode: AlarmMode
    __arm: int

    def __init__(self, mode: AlarmMode = AlarmMode.DISARM, f_arm: int = -1):
        self.__mode = mode
        self.__arm = f_arm


@dataclass()
class AlarmForm:
    pcondform1: AlarmPanel
    pcondform2: AlarmPanel

    def __init__(self, pcondform1: dict = {}, pcondform2: dict = {}):
        self.pcondform1 = AlarmPanel(**pcondform1)
        self.pcondform2 = AlarmPanel(**pcondform2)


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


@dataclass()
class LupuDevice():
    __type: int
    __sid: str
    __name: str
    __battery: Battery
    __tamper: Tamper
    __location: Location
    __bypass: Bypass
    __alarm_status: str
    __rssi: int

    def __init__(self, type: int = -1, sid: str = "", name: str = "", alarm_status: str = "", rssi: int = -1, **kwargs):
        self.__rssi = rssi
        self.__type = type
        self.__sid = sid
        self.__name = name
        self.__alarm_status = alarm_status
        self.__battery = Battery(**kwargs)
        self.__tamper = Tamper(**kwargs)
        self.__location = Location(**kwargs)
        self.__bypass = Bypass(**kwargs)

    @property
    def sid(self):
        return self.__sid

    @property
    def is_alarm(self):
        return self.__alarm_status == "BURGLAR"

    @property
    def battery(self) -> Battery:
        return self.__battery

    @property
    def tamper(self) -> Tamper:
        return self.__tamper

    @property
    def location(self) -> Location:
        return self.__location

    @property
    def bypass(self) -> Bypass:
        return self.__bypass

    @property
    def signal_strength(self) -> int:
        return self.__rssi


# noinspection PyPep8Naming
@dataclass()
class ContactActor(LupuDevice):
    __open_close: int

    def __init__(self, openClose: int = -1, **kwargs):
        super().__init__(**kwargs)
        self.__open_close = openClose


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
    __is_motion: bool

    def __init__(self, alarm_status: str, **kwargs):
        super().__init__(**kwargs)
        self.__is_motion = alarm_status == "DOORBELL"
