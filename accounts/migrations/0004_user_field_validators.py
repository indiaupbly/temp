# Generated manually for user email/phone validators.

import common.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_user_profile_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(max_length=254, unique=True, validators=[common.validators.validate_email]),
        ),
        migrations.AlterField(
            model_name="user",
            name="phone_number",
            field=models.CharField(blank=True, max_length=20, validators=[common.validators.validate_phone]),
        ),
    ]
