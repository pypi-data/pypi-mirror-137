"""Display laptop battery charge and state."""

__program__: str = "bargets-battery"
__author__: str = "Niklas Larsson"
__credits__: list = ["Niklas Larsson"]
__license__: str = "MIT"
__version__: str = "0.1.0a0"
__maintainer__: str = "Niklas Larsson"
__status__: str = "Alpha"

import abc
import logging
import os
import pathlib
import sys
import subprocess

import ruamel.yaml


class Config:
    """For preparing other Config classes."""

    def __init__(self, log: bool=False) -> None:
        """Set up common values for base classes."""
        self._log: bool = log
        self._yaml: object = ruamel.yaml.YAML()
        self._path: object = pathlib.PurePath(f"{pathlib.Path.home()}/.config/bargets/battery.yaml")
        logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging.DEBUG)

    @property
    def log(self) -> bool:
        """Get if logging is on."""
        return self._log

    @log.setter
    def log(self, value) -> None:
        """Set logging on or off."""
        if value not in {True, False}:
            raise ValueError("Log can be either True or False")
        self._log = value


class IndicatorParser(Config):
    """For parsing indicator."""


class PrefixParser(Config):
    """For parsing prefix."""


class SuffixParser(Config):
    """For parsing suffix."""


class SuspendParser(Config):
    """For parsing suspend."""


class MessageParser(Config):
    """For parsing message."""


class SymbolsParser(Config):
    """For parsing symbols."""


class ThresholdsParser(Config):
    """For parsing thresholds."""


class ConfigParser(Config):
    """For reading user configuration."""

    def __init__(self, log: bool=False) -> None:
        """Set up ConfigParser."""
        super().__init__(log=log)
        self._config: object = None
        self._indicator: str = ""
        self._prefix: str = ""
        self._suffix: str = ""
        self._suspend: bool = True
        self._message: str = ""
        self._symbols: dict = dict()
        self._thresholds: dict = dict()

    @property
    def indicator(self) -> str:
        """Get indicator."""
        return self._indicator

    @property
    def symbols(self) -> dict:
        """Get symbols."""
        return self._symbols

    @property
    def thresholds(self) -> dict:
        """Get thresholds."""
        return self._thresholds

    @property
    def prefix(self) -> str:
        """Get prefix."""
        return self._prefix

    @property
    def suffix(self) -> str:
        """Get suffix."""
        return self._suffix

    @property
    def suspend(self) -> bool:
        """Get suspend mode status."""
        return self._suspend

    @property
    def message(self) -> str:
        """Get warning message."""
        return self._message

    def load(self) -> None:
        """Load user config."""
        if pathlib.Path(str(self._path)).exists():
            if self.log:
                logging.debug(f"Loading user config {str(self._path)!r}...")
            with open(str(self._path), "r") as f:
                self._config = self._yaml.load(f)

    def parse(self) -> None:
        """Parse user config."""
        if self._config:
            if self.log:
                logging.debug(f"Parsing user config {str(self._path)!r}...")

            for key, value in self._config.items():
                if key == "indicator":
                    if not isinstance(value, str):
                        raise ValueError("Indicator has to be of type str")
                    self._indicator = value

                elif key == "symbols":
                    if not isinstance(value, ruamel.yaml.comments.CommentedMap):
                        fmt: str = "symbols:\\n 'charging': <val>\\n'discharging': <val>"
                        raise ValueError(f"Symbols must follow format: {fmt}")
                    try:
                        self._symbols["charging"] = value["charging"]
                        self._symbols["discharging"] = value["discharging"]
                    except AttributeError:
                        pass

                elif key == "thresholds":
                    if not isinstance(value, ruamel.yaml.comments.CommentedMap):
                        fmt: str = "thresholds:\\n 'low': <val>\\n'critical': <val>"
                        raise ValueError(f"Thresholds must follow format: {fmt}")
                    try:
                        self._thresholds["low"] = value["low"]
                        self._thresholds["critical"] = value["critical"]
                    except AttributeError:
                        pass

                elif key == "prefix":
                    if not isinstance(value, str):
                        raise ValueError("Prefix has to be of type str")
                    self._prefix = value

                elif key == "suffix":
                    if not isinstance(value, str):
                        raise ValueError("Suffix has to be of type str")
                    self._suffix = value

                elif key == "suspend":
                    if not isinstance(value, bool):
                        raise ValueError("Suspend has to be of type bool")
                    self._suspend = value


class Battery:
    """Represents a battery."""

    def __init__(self, index: int) -> None:
        """
        Set up a battery.

        Parameters:
            index.... The index of a battery, which data is read.
            This index corresponds directly to the acpi -b's
            output; for example, if index specified is 1, then
            the first entry from the output of 'acpi -b' is used, if found.
        """
        if not isinstance(index, int):
            raise ValueError("Index must be of type int")

        self._index: str = index
        self._suspend: bool = True
        self._charges: dict = {"low": False, "critical": False}
        self._thresholds: dict = {"low": 5, "critical": 3}
        self._symbols: dict = {"charging": "↑", "discharging": "↓"}
        self._indicator: str = "%"
        self._state: str = ""
        self._charge: str = ""

        info: object = None

        try:
            cmd: list = ["acpi", "-b"]
            info = subprocess.run(cmd, capture_output=True, text=True)
        except FileNotFoundError:
            self._state = "N/A"
            self._charge = "N/A"

        # Set battery's state (i.e. charging, discharging, not charging etc.)
        if info:
            for idx, line in enumerate(info.stdout.split("\n"), 1):
                if line.startswith("Battery"):
                    if idx == self._index:
                        line = line.lower()
                        data: list = line.split()
                        if "not charging" in line:
                            self._state = " ".join(data[2:4]).replace(",", "")
                        elif "discharging" in line or "charging" in line:
                            self._state = data[2].replace(",", "")
                        del data, line
                        break

        # Set battery's charge
        if info:
            for idx, line in enumerate(info.stdout.split("\n"), 1):
                if line.startswith("Battery"):
                    if idx == self._index:
                        line = line.lower()
                        data: list = line.split()
                        if "not charging" in line:
                            self._charge = data[4].replace(",", "").replace("%", "")
                        elif "discharging" in line or "charging" in line:
                            self._charge = data[3].replace(",", "").replace("%", "")
                        del data, line
                        break

    @property
    def indicator(self) -> str:
        """Get indicator."""
        return self._indicator

    @indicator.setter
    def indicator(self, value: str) -> None:
        """Set indicator."""
        if not isinstance(value, str):
            raise ValueError("Indicator has to be of type str")
        self._indicator = value

    @property
    def suspend(self) -> bool:
        """Get if suspend mode is on."""
        return self._suspend

    @suspend.setter
    def suspend(self, value: bool) -> None:
        """Set suspend mode."""
        if value not in {True, False}:
            raise ValueError("Suspend can be either True or False")
        self._suspend = value

    @property
    def charge(self) -> str:
        """Get battery's charge."""
        return self._charge

    @property
    def low(self) -> bool:
        """Check if battery charge is low."""
        if self._charge:
            if self._charge in {"N/A"}:
                return False
            if int(self._charge) >= 0:
                return int(self._charge) <= self._thresholds["low"]

        return False

    @low.setter
    def low(self, value: int) -> None:
        """Set what the threshold for 'low' is."""
        if not isinstance(value, int):
            raise ValueError("Threshold for 'low' has to be of type integer")
        if value <= 0:
            raise ValueError("Threshold for 'low' has to be greater than zero")
        self._thresholds["low"] = value

    @property
    def critical(self) -> bool:
        """Check if battery charge is critically low."""
        if self._charge:
            if self._charge in {"N/A"}:
                return False
            if int(self._charge) >= 0:
                return int(self._charge) <= self._thresholds["critical"]

        return False

    @critical.setter
    def critical(self, value: int) -> None:
        """Set what the threshold for 'critical' is."""
        if not isinstance(value, int):
            raise ValueError("Threshold for 'critical' has to be of type int")
        if value <= 0:
            raise ValueError("Threshold for 'critical' has to be greater than zero")
        self._thresholds["critical"] = value

    @property
    def charging(self) -> bool:
        """Check if battery is charging."""
        if self._state in {"charging", "discharging", "not charging"}:
            return self._state == "charging"
        return False

    @property
    def symbol(self) -> str:
        """Get a symbol corresponding to battery's state."""
        if self._state in {"charging", "discharging"}:
            return "↑" if self.charging else "↓"
        return ""

    @symbol.setter
    def symbol(self, values: dict) -> None:
        """Set new symbol indicators for charge and discharge states."""
        if not isinstance(values, dict):
            raise ValueError("Symbols must be provided in form of dict")
        try:
            self._symbols["charging"] = values["charging"]
            self._symbols["discharging"] = values["discharging"]
        except KeyError:
            fmt: str = "{'charging': <val>, 'discharging': <val>}"
            raise KeyError(f"Symbols must be given like: {fmt}")


class Notification(abc.ABC):
    """Abstract base class for all sorts of Notification subclasses."""

    @abc.abstractmethod
    def display(self) -> None:
        pass

    @abc.abstractmethod
    def close(self) -> None:
        pass


class WarningNotification(Notification):
    """Warning notifications handler."""

    def __init__(self, language: str) -> None:
        """
        Set up notifications.

        Parameters:
            language.... Language in which to display warning messages.
        """
        self._language: str = language
        self._message: str = "WARNING: LOW BATTERY CHARGE"
        self._pending: int = 0
        self._nserver: bool = True  # Notification server

        data: object = None

        try:
            cmds: list = ["dunstctl", "count", "displayed"]
            data = subprocess.run(cmds, capture_output=True, text=True)
            self._pending = int(data.stdout.split("\n")[0])
        except FileNotFoundError:
            self._nserver = False

    def display(self) -> None:
        """Display warning notification."""
        if self._language == "fi_FI.UTF-8":
            self._message = "VAROITUS: AKUN TASO MATALA"
        if self._nserver:
            subprocess.run(["notify-send", "--urgency", "critical", self._message])

    def close(self) -> None:
        """Close warning messages."""
        if self._nserver:
            subprocess.run(["dunstctl", "close"])

    @property
    def message(self) -> str:
        """Get warning message."""
        return self._message

    @message.setter
    def message(self, new: str) -> None:
        """Set new warning message."""
        if not isinstance(new, str):
            raise ValueError("Warning message has to be of type str")
        self._message = new

    @property
    def pending(self) -> bool:
        """Check if any pending notifications exist."""
        return self._pending > 0


def main() -> None:
    """Main function."""

    language: str = os.environ["LANG"]
    warnings: object = WarningNotification(language)
    batteries: list = [Battery(b) for b in range(1, 3)]

    # Display battery data
    for idx, i in enumerate(batteries):
        if 0 < idx < len(batteries):
            print(" ", end="")
        print(f"{i.symbol}{i.charge}{i.indicator}", end="")
    print()

    # Suspend system if the last (or in this case the "first")
    # battery is running on critically low charge. I'm not sure
    # in what order batteries are usually used, but it seems that
    # at least on my Thinkpad X240 (has internal battery + external
    # one) the inner battery is used first (I guess?), and then the
    # outer one.
    if batteries[0].critical and batteries[0].suspend:
        subprocess.run(["systemctl", "suspend"])

    # Display warning if last battery is running on low charge
    if not any([battery.charging for battery in batteries]):
        if batteries[0].low:
            if not warnings.pending:
                warnings.display()
                sys.exit(0)

    # Close warnings when plugging a charger
    if warnings.pending:
        warnings.close()


if __name__ == "__main__":
    main()
