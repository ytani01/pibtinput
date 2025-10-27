#
# (c) 2025 Yoichi Tanibayashi
#
import evdev

from .utils.mylogger import errmsg, get_logger


class PiBtInput:
    """Bluetooth input."""

    def __init__(self, debug=False) -> None:
        self.__debug = debug
        self.__log = get_logger(self.__class__.__name__, self.__debug)
        self.__log.debug("")

    def search_input_devs(self, dev_words: list[str]) -> list:
        """Search device"""
        self.__log.debug("dev_words=%s", dev_words)

        ret_devs = []

        for d in evdev.util.list_devices():
            _input_dev = evdev.device.InputDevice(d)
            self.__log.debug("_input_dev=%s", _input_dev)

            dev_found: evdev.device.InputDevice[str] | None = _input_dev
            for w in dev_words:
                if w not in _input_dev.name:
                    dev_found = None
                    break

            if dev_found:
                ret_devs.append(dev_found)

        return ret_devs

    def get_key_event(self, ev):
        """Get key event."""
        self.__log.debug("ev=%s", ev)

        if ev.type != evdev.ecodes.EV_KEY:
            self.__log.debug("ignore: ev.type=%s", ev.type)
            return None, None

        key_name = evdev.ecodes.keys[ev.code]
        self.__log.debug("key_name=%s", key_name)

        key_state = evdev.KeyEvent(ev).keystate
        self.__log.debug("key_state=%s", key_state)

        return key_name, key_state

    def read_loop(self, dev, cb_key_event):
        """Read loop."""
        self.__log.debug("dev=%s, cb_key_event=%s", dev, cb_key_event)

        if not cb_key_event:
            self.__log.warning("cb_key_event=%s", cb_key_event)
            return

        try:
            for ev in dev.read_loop():
                key_name, key_state = self.get_key_event(ev)
                if not key_name:
                    continue

                cb_key_event(key_name, key_state)

        except Exception as e:
            self.__log.error(errmsg(e))
