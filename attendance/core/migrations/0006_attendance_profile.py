# Generated by Django 4.0.5 on 2023-02-18 08:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0004_initial'),
        ('core', '0005_remove_attendance_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='userprofile.userprofile'),
        ),
    ]
