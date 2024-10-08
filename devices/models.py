from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.

class Location(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Device(models.Model):
    class DeviceType(models.TextChoices):
        RELAY = 'relay', _('Relay')
        RELAY_PERIODIC = 'relay-periodic', _('Periodic relay')

    class ControlInputParams:
        def __init__(self, input_type: str, label: str = None, params: dict = ()):
            self.type = input_type
            self.label = label
            self.params = params

        def __eq__(self, other):
            return self.type == other.type and self.label == other.label and self.params == other.params

    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20,
                            choices=DeviceType.choices)
    config_file = models.CharField(max_length=100)

    def __str__(self):
        return (f"{self.name}: "
                f"type={self.type}, "
                f"config_file={self.config_file}")


class RelayPeriodicPeriod(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    begin = models.TimeField()
    end = models.TimeField()

    def get_begin_display(self):
        return self.begin.strftime('%H:%M')

    def get_end_display(self):
        return self.end.strftime('%H:%M')

    def __str__(self):
        return (f"{self.device.name}: "
                f"begin={self.begin}, "
                f"end={self.end}")


class RelayPeriodicDay(models.Model):
    class DaysChoices(models.IntegerChoices):
        MONDAY = 0, _('Monday')
        TUESDAY = 1, _('Tuesday')
        WEDNESDAY = 2, _('Wednesday')
        THURSDAY = 3, _('Thursday')
        FRIDAY = 4, _('Friday')
        SATURDAY = 5, _('Saturday')
        SUNDAY = 6, _('Sunday')

    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    day = models.IntegerField(choices=DaysChoices)

    def __str__(self):
        return (f"{self.device.name}: "
                f"day={self.day}")


class RelayPeriodicManualActivation(models.Model):
    device = models.OneToOneField(Device, on_delete=models.CASCADE)
    end_time = models.DateTimeField()

    def __str__(self):
        return (f"{self.device.name}: "
                f"end_time={self.end_time}")
