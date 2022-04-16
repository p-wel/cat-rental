# Generated by Django 3.2.11 on 2022-03-24 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cats', '0008_rental_valid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rental',
            name='valid',
        ),
        migrations.AddField(
            model_name='rental',
            name='status',
            field=models.CharField(default='No status', max_length=50),
        ),
    ]
