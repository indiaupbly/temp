# Generated manually for adding user profile images.

import common.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_alter_user_managers_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="profile_image",
            field=models.ImageField(blank=True, null=True, upload_to="users/profile_images/", validators=[common.validators.validate_image_file]),
        ),
    ]
