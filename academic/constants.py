from django.db import models


class HolidayTypeChoices(models.TextChoices):
    HOLIDAY = "HOLIDAY", "Holiday"
    SUNDAY = "SUNDAY", "Sunday"
    NON_WORKING_DAY = "NON_WORKING_DAY", "Non Working Day"
