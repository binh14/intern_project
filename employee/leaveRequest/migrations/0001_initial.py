# Generated by Django 5.0.1 on 2024-01-26 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LeaveRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('status', models.CharField(max_length=255)),
                ('rejected_reason', models.CharField(max_length=255)),
                ('other', models.CharField(max_length=255)),
                ('reason', models.CharField(choices=[('SICK', 'Sick'), ('VACATION', 'Vacation'), ('OFFICE MOVEMENT', 'Office Movement'), ('FAMILY', 'Family'), ('BUSINESS TRIP', 'Business'), ('URGENT CARE', 'Urgent Care'), ('ACCIDENT', 'Accident'), ('APPOIMENT', 'Appoiment'), ('NO_PERMISSION', 'No Permission'), ('OTHER', 'Other')], default='NO_PERMISSION', max_length=255)),
            ],
        ),
    ]
