# Generated by Django 5.0.1 on 2024-01-30 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaveRequest', '0002_rename_other_leaverequest_other_reaoson_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='leaverequest',
            old_name='other_reaoson',
            new_name='other_reason',
        ),
        migrations.AlterField(
            model_name='leaverequest',
            name='reason',
            field=models.CharField(choices=[('SICK', 'Sick'), ('VACATION', 'Vacation'), ('FAMILY', 'Family'), ('ACCIDENT', 'Accident'), ('NO_PERMISSION', 'No Permission'), ('OTHER', 'Other')], default='NO_PERMISSION', max_length=255),
        ),
    ]
