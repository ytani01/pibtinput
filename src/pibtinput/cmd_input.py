#
# (c) 2025 Yoichi Tanibayashi
#

import evdev

from .pibtinput import PiBtInput
from .utils.mylogger import get_logger


class CmdInput:
    """Test."""

    def __init__(self, dev_words, flag_repeat=False, debug=False) -> None:
        self.__debug = debug
        self.__log = get_logger(self.__class__.__name__, self.__debug)
        self.__log.debug(
            "dev_words=%s, flag_repeat=%s", dev_words, flag_repeat
        )

        self.dev_words = dev_words
        self.flag_repeat = flag_repeat

        self.prev_onkeys: dict[str, int] = {}

        self.bt = PiBtInput(self.__debug)

    def cb_ev(self, key_name, key_state, onkeys):
        """Event Callback."""
        self.__log.debug(
            "key_name=%s,key_state=%s,onkeys=%s", key_name, key_state, onkeys
        )

        if onkeys != self.prev_onkeys:
            self.__log.debug(f"{self.prev_onkeys} -> {onkeys}")
            self.prev_onkeys = onkeys.copy()

            if onkeys.get("KEY_S"):
                if onkeys["KEY_S"] > 10:
                    print("Bye !")
                    return False

            if key_state == evdev.KeyEvent.key_hold and not self.flag_repeat:
                return True

            print(f"{key_name}:{key_state}  {onkeys}")

        return True

    def main(self):
        """Main."""
        self.__log.debug("")

        input_dev = self.bt.search_input_devs(self.dev_words)
        if not input_dev:
            self.__log.error("no such device: %s", list(self.dev_words))
            return

        if len(input_dev) > 1:
            self.__log.error("ambiguous: %s", [d.name for d in input_dev])
            return

        print(f"input_dev: {input_dev[0]}")
        print("* long press 'S' to exit.")
        self.bt.read_loop(input_dev[0], self.cb_ev)

    def end(self):
        """End."""
        self.__log.debug("")
