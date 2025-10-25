#
# (c) 2025 Yoichi Tanibayashi
#
import evdev

from .utils.mylogger import get_logger


class CmdInput:
    """Test."""

    def __init__(self, dev_name, debug=False) -> None:
        self.__debug = debug
        self.__log = get_logger(self.__class__.__name__, self.__debug)
        self.__log.debug("dev_name=%s", dev_name)

        self.dev_name = dev_name

    def main(self):
        """Main."""
        self.__log.debug("")

        input_dev = None
        devs = evdev.util.list_devices()
        for d in sorted(devs):
            _indev = evdev.device.InputDevice(d)
            if self.dev_name in _indev.name:
                input_dev = _indev
                break

        print(f"input_dev={input_dev}")

        if input_dev:
            prev_on_keys = []
            on_keys = []
            for ev in input_dev.read_loop():
                if ev.type != evdev.ecodes.EV_KEY:
                    continue
                key_ev = evdev.KeyEvent(ev)
                key_name = evdev.ecodes.keys[ev.code]

                if key_ev.keystate == evdev.KeyEvent.key_down:
                    on_keys.append(key_name)
                    on_keys = sorted(list(set(on_keys)))
                elif key_ev.keystate == evdev.KeyEvent.key_up:
                    on_keys.remove(key_name)
                else:
                    continue

                if on_keys != prev_on_keys:
                    print(on_keys)
                    prev_on_keys = []
                    for k in on_keys:
                        prev_on_keys.append(k)

    def end(self):
        """End."""
        self.__log.debug("")
