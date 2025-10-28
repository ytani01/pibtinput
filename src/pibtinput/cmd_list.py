#
# (c) 2025 Yoichi Tanibayashi
#

from .pibtinput import PiBtInput
from .utils.mylogger import get_logger


class CmdList:
    """Test."""

    def __init__(self, words, debug=False) -> None:
        self.__debug = debug
        self.__log = get_logger(self.__class__.__name__, self.__debug)
        self.__log.debug("words=%s", words)

        self.words = words
        self.bt = PiBtInput(debug=self.__debug)

    def main(self):
        self.__log.debug("")

        devs = self.bt.search_input_devs(self.words)
        for d in sorted(devs, key=lambda x: x.path):
            print(f"{d}")

    def end(self):
        self.__log.debug("")
