#
# (c) 2025 Yoichi Tanibayashi
#
import evdev

from .pibtinput import PiBtInput
from .utils.mylogger import get_logger


class CmdInput:
    """Test."""

    def __init__(self, dev_words, debug=False) -> None:
        self.__debug = debug
        self.__log = get_logger(self.__class__.__name__, self.__debug)
        self.__log.debug("dev_words=%s", dev_words)

        self.dev_words = dev_words

        self.onkeys: list[str] = []
        self.prev_onkeys: list[str] = []

        self.bt = PiBtInput(self.__debug)

    def cb_ev(self, key_name, key_state):
        """Event Callback."""
        self.__log.debug("key_name=%s, key_state=%s", key_name, key_state)

        if key_state == evdev.KeyEvent.key_down:
            # キーが押下されたら、self.onkeysに加える
            self.onkeys.append(key_name)
            self.onkeys = sorted(list(set(self.onkeys)))

        elif key_state == evdev.KeyEvent.key_up:
            # キーが放されたら、self.onkeysから削除する
            self.onkeys.remove(key_name)

        else:
            # リピートなどは無視
            return

        if self.onkeys != self.prev_onkeys:
            print(f"{key_name}:{key_state}  {self.onkeys}")
            self.prev_onkeys = self.onkeys.copy()

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
        self.bt.read_loop(input_dev[0], self.cb_ev)

    def end(self):
        """End."""
        self.__log.debug("")
