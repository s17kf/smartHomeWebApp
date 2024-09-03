import json
from .models import Device, RelayPeriodicPeriod, RelayPeriodicDay
import gpiocontrol as gpio


class DeviceConfig:

    def __init__(self, device: Device):
        self.device = device

    @staticmethod
    def parse_device(device: Device):
        match device.type:
            case Device.DeviceType.RELAY:
                return RelayDeviceConfig(device)
            case Device.DeviceType.RELAY_PERIODIC:
                return RelayPeriodicDeviceConfig(device)
        return UnknownTypeDeviceConfig(device, device.type)

    def get_details_template(self):
        return "devices/details/not_implemented_details.html"

    def get_status_template(self):
        return "devices/details/not_implemented_status.html"


class RelayDeviceConfig(DeviceConfig):
    def __init__(self, device: Device):
        assert device.type == Device.DeviceType.RELAY
        super().__init__(device)
        self.state_available = False
        try:
            config_file = open(device.config_file)
            self.config = json.load(config_file)
        except IOError:
            self.config = None
            return
        try:
            self.pin_number = self.config["pinNumber"]
            self.state = gpio.get(self.pin_number)
        except Exception:
            # todo: log error
            return
        self.state_available = True

    def is_active(self):
        return self.state == gpio.State.LOW

    def get_status_template(self):
        return "devices/details/relay_status.html"

    def setstate(self, state: gpio.State):
        try:
            gpio.set(self.pin_number, state)
        except Exception:
            # todo: log error
            pass


class RelayPeriodicDeviceConfig(DeviceConfig):
    def __init__(self, device: Device):
        assert device.type == Device.DeviceType.RELAY_PERIODIC
        super().__init__(device)
        self.state_available = False
        try:
            config_file = open(device.config_file)
            self.config = json.load(config_file)
        except IOError:
            self.config = None
            return
        try:
            self.pin_number = self.config["pinNumber"]
            self.state = gpio.get(self.pin_number)
        except Exception:
            # todo: log error
            return
        self.state_available = True

    def is_active(self):
        return self.state == gpio.State.LOW

    def get_active_days(self):
        return RelayPeriodicDay.objects.filter(device=self.device)

    def get_active_periods(self):
        return RelayPeriodicPeriod.objects.filter(device=self.device)

    def get_details_template(self):
        return "devices/details/relay_periodic_details.html"

    def get_status_template(self):
        return "devices/details/relay_periodic_status.html"


class MissingConfigFileDeviceConfig(DeviceConfig):
    def __init__(self, device: Device):
        super().__init__(device)


class UnknownTypeDeviceConfig(DeviceConfig):
    def __init__(self, device: Device, type: str):
        super().__init__(device)
        self.type = type
