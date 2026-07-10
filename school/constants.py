from django.db import models


class BoardChoices(models.TextChoices):
    CBSE = "CBSE", "CBSE"
    ICSE = "ICSE", "ICSE"
    STATE = "STATE_BOARD", "State Board"
    IB = "IB", "IB"
    CAMBRIDGE = "CAMBRIDGE", "Cambridge"
    OTHER = "OTHER", "Other"


class SchoolTypeChoices(models.TextChoices):
    PRIVATE = "PRIVATE", "Private"
    GOVERNMENT = "GOVERNMENT", "Government"
    SEMI_GOVERNMENT = "SEMI_GOVERNMENT", "Semi Government"
