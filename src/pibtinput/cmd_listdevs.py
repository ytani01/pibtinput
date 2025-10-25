#
# (c) 2025 Yoichi Tanibayashi
#
import evdev

from .utils.mylogger import get_logger


class CmdListDevs:
    """Test."""

    def __init__(self, debug=False) -> None:
        self.__debug = debug
        self.__log = get_logger(self.__class__.__name__, self.__debug)
        self.__log.debug("")

    def main(self):
        self.__log.debug("")

        devs = evdev.util.list_devices()
        for d in sorted(devs):
            dev_info = evdev.device.InputDevice(d)
            print(f"{dev_info}")

    def end(self):
        self.__log.debug("")
