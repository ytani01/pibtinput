#
# (c) 2025 Yoichi Tanibayashi
#
import evdev

from .utils.mylogger import get_logger


class CmdInput:
    """Test."""

    def __init__(self, dev_words, debug=False) -> None:
        self.__debug = debug
        self.__log = get_logger(self.__class__.__name__, self.__debug)
        self.__log.debug("dev_words=%s", dev_words)

        self.dev_words = dev_words

    def search_dev(self, dev_words):
        """Search device."""
        self.__log.debug("dev_words=%s", dev_words)

        input_dev = None
        devs = evdev.util.list_devices()
        for d in sorted(devs):
            _inputdev = evdev.device.InputDevice(d)
            self.__log.debug("_inputdev=%s", _inputdev)

            input_dev = _inputdev
            for w in self.dev_words:
                if w not in _inputdev.name:
                    input_dev = None
                    break
            if input_dev:
                break

        return input_dev

    def get_key_event(self, ev):
        """Get event key name."""
        self.__log.debug("ev=%s", ev)

        if ev.type != evdev.ecodes.EV_KEY:
            self.__log.debug("ignore: ev.type=%s", ev.type)
            return None, None

        key_name = evdev.ecodes.keys[ev.code]
        self.__log.debug("key_name=%s", key_name)

        key_state = evdev.KeyEvent(ev).keystate
        self.__log.debug("key_state=%s", key_state)

        return key_name, key_state

    def main(self):
        """Main."""
        self.__log.debug("")

        input_dev = self.search_dev(self.dev_words)
        if input_dev is None:
            self.__log.error("no such device: %s", self.dev_words)
            return

        print(f"input_dev: {input_dev}")

        on_keys = []
        prev_on_keys = []
        for ev in input_dev.read_loop():
            key_name, key_state = self.get_key_event(ev)
            if not key_name:
                continue

            if key_state == evdev.KeyEvent.key_down:
                # キーが押下されたら、on_keysに加える
                on_keys.append(key_name)
                on_keys = sorted(list(set(on_keys)))

            elif key_state == evdev.KeyEvent.key_up:
                # キーが放されたら、on_keysから削除する
                on_keys.remove(key_name)

            else:
                # リピートなどは無視
                continue

            if on_keys != prev_on_keys:
                print(f"{key_name}:{key_state}  {on_keys}")
                prev_on_keys = on_keys.copy()

    def end(self):
        """End."""
        self.__log.debug("")
