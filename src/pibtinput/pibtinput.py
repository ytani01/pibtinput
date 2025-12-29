#
# (c) 2025 Yoichi Tanibayashi
#
import queue
import threading

import evdev

from .utils.mylogger import errmsg, get_logger


class PiBtInput(threading.Thread):
    """Bluetooth input."""

    KEY = {
        "down": evdev.KeyEvent.key_down,
        "hold": evdev.KeyEvent.key_hold,
        "up": evdev.KeyEvent.key_up,
    }
    Q_TIMEOUT = 0.1

    def __init__(self, debug=False) -> None:
        super().__init__(daemon=True)
        self.__debug = debug
        self.__log = get_logger(self.__class__.__name__, self.__debug)
        self.__log.debug("")

        # {'KEY_?': 1, 'KEY_?': 20, ...}
        self.onkeys: dict[str, int] = {}

        self.in_q: queue.SimpleQueue = queue.SimpleQueue()
        self.is_active = False
        self.is_busy = False  # 処理中、または、キューに残っている
        self.cb_key_event = None  # calllback function

    def end(self):
        """End."""
        self.__log.debug("")

        self.is_active = False
        self.clear_q()
        self.join()
        self.__log.debug("done.")

    def read_loop(self, dev, cb_key_event):
        """Read loop."""
        self.__log.debug("dev=%s, cb_key_event=%s", dev, cb_key_event)

        # self.onkeys.clear()

        self.cb_key_event = cb_key_event

        self.start()

        try:
            for ev in dev.read_loop():
                self.__log.debug("ev=%s", ev)
                self.in_q.put(ev)

        except Exception as e:
            self.__log.error(errmsg(e))

        self.end()

    def clear_q(self):
        """Clear queue."""

        _count = 0
        while not self.in_q.empty():
            _count += 1
            _ = self.in_q.get()

        self.__log.debug("_count=%s", _count)
        return _count

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

    @property
    def qsize(self) -> int:
        """queue size."""
        return self.in_q.qsize()

    def run(self):
        """Thread: run."""
        self.__log.debug("")

        if self.qsize == 0:
            self.is_busy = False

        self.is_active = True
        while self.is_active:
            try:
                event = self.in_q.get(timeout=self.Q_TIMEOUT)
            except queue.Empty:
                continue

            self.is_busy = True

            key_name, key_state = self.get_key_event(event)
            if not key_name:
                continue

            self.__log.debug(
                "qsize=%s,key_name=%a,key_state=%s",
                self.in_q.qsize(),
                key_name,
                key_state,
            )

            if key_state == evdev.KeyEvent.key_down:
                # キーが押下されたら、self.onkeysに加える
                self.onkeys[key_name] = 1

            if key_state == evdev.KeyEvent.key_hold:
                # リピート
                self.onkeys[key_name] += 1

            if key_state == evdev.KeyEvent.key_up:
                # キーが放されたら、self.onkeysから削除する
                try:
                    del self.onkeys[key_name]
                except KeyError as e:
                    self.__log.warning(errmsg(e))

            if self.cb_key_event is not None:
                self.is_active = self.cb_key_event(
                    key_name, key_state, self.onkeys
                )

            self.__log.info("is_active=%s", self.is_active)

        self.__log.debug("done.")
