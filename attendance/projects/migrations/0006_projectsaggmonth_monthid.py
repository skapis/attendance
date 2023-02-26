# Generated by Django 4.0.5 on 2023-02-19 16:59

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_projectsaggmonth'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectsaggmonth',
            name='monthId',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]
