# Generated by Django 3.2.7 on 2022-07-02 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cats', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rental',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Not activate (draft)'), (1, 'Pending (@)'), (2, 'Active'), (3, 'Finished'), (4, 'Cancelled')], default=0),
        ),
    ]