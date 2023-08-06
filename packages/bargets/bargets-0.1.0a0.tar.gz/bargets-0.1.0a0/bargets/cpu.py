"""Display cpu temperature."""

__program__: str = "bargets-cpu"
__author__: str = "Niklas Larsson"
__credits__: list = ["Niklas Larsson"]
__license__: str = "MIT"
__version__: str = "0.1.0a0"
__maintainer__: str = "Niklas Larsson"
__status__: str = "Alpha"

import logging
import pathlib
import subprocess

import ruamel.yaml


class Config:
    """For preparing other Config classes."""

    def __init__(self, log: bool=False) -> None:
        """Set up common values for base classes."""
        self._log: bool = log
        self._yaml: object = ruamel.yaml.YAML()
        self._path: object = pathlib.PurePath(f"{pathlib.Path.home()}/.config/bargets/cpu.yaml")
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


class ConfigParser(Config):
    """For reading user configuration."""

    def __init__(self, log: bool=False) -> None:
        """Set up ConfigParser."""
        super().__init__(log=log)
        self._config: object = None
        self._unit: str = "celcius"
        self._indicator: str = "°C"
        self._prefix: str = ""
        self._suffix: str = ""

    @property
    def unit(self) -> str:
        """Get temperature unit."""
        return self._unit

    @property
    def indicator(self) -> str:
        """Get indicator."""
        return self._indicator

    @property
    def prefix(self) -> str:
        """Get prefix."""
        return self._prefix

    @property
    def suffix(self) -> str:
        """Get suffix."""
        return self._suffix

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
                if key == "unit":
                    self._unit = value
                elif key == "indicator":
                    self._indicator = value
                elif key == "prefix":
                    self._prefix = value
                elif key == "suffix":
                    self._suffix = value


class CPUTemperature:
    """Represents the CPU temperatures."""

    def __init__(self) -> None:
        """Set up cpu data."""
        self._unit: str = "celcius"
        self._temp: str = ""
        self._indicator: str = "°C"
        self._prefix: str = ""
        self._suffix: str = ""

        data: object = None

        try:
            cmd: list = ["sensors"]
            data = subprocess.run(cmd, capture_output=True, text=True)
        except FileNotFoundError:
            self._temp = "N/A"

        # Set temperature
        if data:
            for row in data.stdout.split("\n"):
                if row.startswith("CPU"):
                    for field in row.split():
                        if "°C" in field:
                            self._temp = field.replace("+", "").replace("°C", "")
                            break
                        elif "°F" in field:
                            self._temp = field.replace("+", "").replace("°F", "")
                            break

    @property
    def suffix(self) -> str:
        """Get suffix that is displayed after temperature reading."""
        return self._suffix

    @suffix.setter
    def suffix(self, value: str) -> str:
        """Set suffix."""
        if not isinstance(value, str):
            raise ValueError("Suffix has to be of type str")
        self._suffix = value

    @property
    def prefix(self) -> str:
        """Get prefix that is displayed before cpu temperature reading."""
        return self._prefix

    @prefix.setter
    def prefix(self, value: str) -> None:
        """Set prefix."""
        if not isinstance(value, str):
            raise ValueError("Prefix has to be a string")
        self._prefix = value

    @property
    def indicator(self) -> str:
        """Get indicator that is used next to temperature."""
        return self._indicator

    @indicator.setter
    def indicator(self, value: str) -> None:
        """Set indicator."""
        if not isinstance(value, str):
            raise ValueError("Symbol has to be of type str")
        self._indicator = value

    @property
    def temp(self) -> str:
        """Get cpu temperature."""
        # Due to floating point errors, round temp with 1 decimal precision
        return round(float(self._temp), 1)

    @property
    def unit(self) -> str:
        """Get temperature measurement unit."""
        return self._unit

    @unit.setter
    def unit(self, value: str) -> None:
        """Set temperature measurement unit. Convert temp if necessary."""

        if value not in {"fahrenheit", "celcius"}:
            raise ValueError("Unit can be either celcius of fahrenheit")

        if self._unit == "celcius" and value == "fahrenheit":
            self._unit = value
            self._indicator = "°F"
            self._temp = str(float((float(self._temp) * 1.8) + 32))

        if self._unit == "fahrenheit" and value == "celcius":
            self._unit = value
            self._indicator = "°C"
            self._temp = str(float((float(self._temp) -32) / 1.8))


def main() -> None:
    """Main function."""

    cpu: object = CPUTemperature()
    cparser: object = ConfigParser(log=True)
    cparser.log = False

    print(f"{cpu.prefix}{cpu.temp}{cpu.indicator}{cpu.suffix}")


if __name__ == "__main__":
    main()
