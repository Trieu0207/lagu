# Generated by Django 4.2.5 on 2023-10-09 14:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lagu', '0016_alter_hoadoncoctien_ngay_thanh_toan_alter_menu_loai'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hoadoncoctien',
            name='ngay_thanh_toan',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 9, 21, 41, 19, 532591)),
        ),
    ]
