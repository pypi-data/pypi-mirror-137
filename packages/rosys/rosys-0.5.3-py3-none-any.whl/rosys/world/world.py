from pydantic import BaseModel, PrivateAttr
from aenum import Enum, auto
import time
from .area import Area
from .camera import Camera
from .mode import Mode
from .obstacle import Obstacle
from .robot import Robot
from .upload import Upload
from .usb_camera import UsbCamera


class AutomationState(str, Enum, init='value __doc__'):

    def _generate_next_value_(name, start, count, last_values):
        '''uses enum name as value when calling auto()'''
        return name

    DISABLED = auto(), 'no automations available or execution not allowed'
    STOPPED = auto(), 'there is an automation which could be started'
    RUNNING = auto(), 'automations are beeing processed'
    PAUSED = auto(), 'an ongoing automation can be resumed'


class World(BaseModel):
    robot: Robot = Robot()
    mode: Mode = Mode.REAL
    automation_state: AutomationState = AutomationState.DISABLED
    _time: float = PrivateAttr(default_factory=time.time)
    obstacles: dict[str, Obstacle] = {}
    areas: dict[str, Area] = {}
    notifications: list[tuple[float, str]] = []
    usb_cameras: dict[str, UsbCamera] = {}
    upload: Upload = Upload()

    @property
    def time(self):
        return self._time if self.mode == Mode.TEST else time.time()

    def set_time(self, value):
        assert self.mode == Mode.TEST
        self._time = value

    @property
    def cameras(self) -> dict[str, Camera]:
        return self.usb_cameras
