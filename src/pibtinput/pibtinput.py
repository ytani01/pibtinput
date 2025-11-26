#
# (c) 2025 Yoichi Tanibayashi
#

import evdev

from .utils.mylogger import get_logger


class PiBtInput:
    """Bluetooth input."""

    KEY = {
        "down": evdev.KeyEvent.key_down,
        "hold": evdev.KeyEvent.key_hold,
        "up": evdev.KeyEvent.key_up,
    }

    def __init__(self, debug=False) -> None:
        self.__debug = debug
        self.__log = get_logger(self.__class__.__name__, self.__debug)
        self.__log.debug("")

        # {'KEY_?': 1, 'KEY_?': 20, ...}
        self.onkeys: dict[str, int] = {}

    def list_input_devs(self):
        """List input devices."""
        self.__log.debug("")

        input_devs = [
            evdev.device.InputDevice(d) for d in evdev.util.list_devices()
        ]
        self.__log.debug("input_devs=%s", input_devs)
        return input_devs

    def list_keyin_devs(self):
        """List key input devices."""

        in_devs = self.list_input_devs()

        keyin_devs = []
        for d in in_devs:
            if evdev.ecodes.EV_KEY in d.capabilities():
                keyin_devs.append(d)

        self.__log.debug("keyin_devs=%s", keyin_devs)
        return keyin_devs

    def search_input_devs(self, search_keywords: list[str]) -> list:
        """Search device"""
        self.__log.debug("search_keywords=%s", search_keywords)

        keyin_devs = self.list_keyin_devs()
        if not search_keywords:
            return keyin_devs

        ret_devs = []

        for _dev in keyin_devs:
            dev_found: evdev.device.InputDevice[str] | None = _dev
            for w in search_keywords:
                if w not in _dev.name:
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

        key_name = evdev.ecodes.keys[ev.code]  # str | Tuple[str]
        if isinstance(key_name, tuple):
            key_name = key_name[0]
        self.__log.debug("key_name=%s", key_name)

        key_state = evdev.KeyEvent(ev).keystate
        self.__log.debug("key_state=%s", key_state)

        return key_name, key_state

    def read_loop(self, dev, cb_key_event):
        """Read loop."""
        self.__log.debug("dev=%s, cb_key_event=%s", dev, cb_key_event)

        self.onkeys.clear()

        if not cb_key_event:
            self.__log.error("cb_key_event=%s", cb_key_event)
            return

        for ev in dev.read_loop():
            key_name, key_state = self.get_key_event(ev)
            if not key_name:
                continue

            if key_state == evdev.KeyEvent.key_down:
                # キーが押下されたら、self.onkeysに加える
                self.onkeys[key_name] = 1

            if key_state == evdev.KeyEvent.key_hold:
                # リピート
                self.onkeys[key_name] += 1

            if key_state == evdev.KeyEvent.key_up:
                # キーが放されたら、self.onkeysから削除する
                del self.onkeys[key_name]

            ret = cb_key_event(key_name, key_state, self.onkeys)
            if not ret:
                break
